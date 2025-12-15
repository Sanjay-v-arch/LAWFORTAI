from nlp.engine import fuzzy_search

queries = [
    "AI deepfake harassment",
    "phishing email attack",
    "IoT botnet attack",
    "health data privacy",
    "ransomware deployment"
]

for q in queries:
    law, score, method = fuzzy_search(q)
    print(q, "=>", law["title"] if law else "No match", score)
