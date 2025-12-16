# chatbot.py

import json
import os
from nlp.fuzzy_match import fuzzy_search
from nlp.semantic_match import semantic_search
from presets import PRESET_RESPONSES
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import torch

# ---------------- Setup ----------------
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "log.json")

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set your GEMINI_API_KEY in a .env file!")

# ---------------- Load Hugging Face model ----------------
HF_MODEL_NAME = "distilgpt2"  # lightweight GPT2 variant
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(HF_MODEL_NAME).to(device)

# Ensure pad_token_id is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# ---------------- Preset response check ----------------
def get_preset_response(query: str):
    query_lower = query.lower()
    for key, response in PRESET_RESPONSES.items():
        if key in query_lower:
            return response
    return None

# ---------------- Law search (Hybrid) ----------------
def get_law_response(query: str):
    # 1️⃣ Fuzzy search
    law, score, method = fuzzy_search(query)
    if law:
        return f"Law Found (Fuzzy Match - {score:.2f}): {law['act']} - Section {law.get('section','')}: {law.get('title','')}", True

    # 2️⃣ Semantic search
    law, score, method = semantic_search(query)
    if law:
        return f"Law Found (Semantic Match - {score:.2f}): {law['act']} - Section {law.get('section','')}: {law.get('title','')}", True

    # 3️⃣ Not found
    return None, False

# ---------------- Google Gemini LLM generation ----------------
def get_gemini_response(query: str):
    url = "https://api.generativeai.google/v1beta2/models/text-bison-001:generate"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "prompt": query,
        "temperature": 0.7,
        "max_output_tokens": 200
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", None)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Gemini API unreachable: {e}")
        return None

# ---------------- Hugging Face fallback ----------------
def get_hf_response(query: str):
    inputs = tokenizer.encode(query, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs,
        max_length=150,         # slightly longer for more complete answers
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id  # avoids warnings about pad token
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean up the response
    text = text.strip()                    # remove leading/trailing spaces
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())  # remove empty lines
    text = text.replace("\n\n\n", "\n")   # replace multiple newlines with single newline

    # Optionally, truncate to 300 chars to keep chat-friendly
    if len(text) > 300:
        text = text[:300].rsplit(" ", 1)[0] + "…"

    return text


# ---------------- Logging ----------------
def log_query(query: str, response: str):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append({"query": query, "response": response})
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
    print(f"📄 Logs saved to {LOG_FILE}")

# ---------------- Main chatbot response ----------------
def chatbot_response(query: str):
    # 0️⃣ Empty / whitespace query check (IMPORTANT)
    if not query or not query.strip():
        response = "Please enter a valid question 🙂"
        log_query(query, response)
        return response

    # 1️⃣ Preset response
    preset = get_preset_response(query)
    if preset:
        log_query(query, preset)
        return preset

    # 2️⃣ Law-related response
    law_resp, found = get_law_response(query)
    if found:
        log_query(query, law_resp)
        return law_resp

    # 3️⃣ Google Gemini
    gemini_resp = get_gemini_response(query)
    if gemini_resp:
        log_query(query, gemini_resp)
        return gemini_resp

    # 4️⃣ Hugging Face fallback
    hf_resp = get_hf_response(query)
    log_query(query, hf_resp)
    return hf_resp


# ---------------- CLI interface ----------------
if __name__ == "__main__":
    print("⚖️ LawFort ChatBot is online! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("ChatBot: Bye! 👋")
            break
        response = chatbot_response(user_input)
        print(f"ChatBot: {response}")
