from chatbot import process_user_query

print("Bot: Hello! I can answer law questions or chat with you. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Bye! See you later.")
        break

    answer = process_user_query(user_input)
    print(f"Bot: {answer}\n")
