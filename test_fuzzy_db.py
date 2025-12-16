from nlp.engine import process_query

queries = [
    "company leaking personal data",
    "user consent violation",
    "unauthorized data processing",
    "random football question"
]

for q in queries:
    law, score, method = process_query(q)
    print(f"\nQuery: {q}")
    print(f"Method: {method}")
    print(f"Score: {score}")
    print(f"Law: {law}")
