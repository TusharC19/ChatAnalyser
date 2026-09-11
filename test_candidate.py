import preprocessor
from ai.candidate_filter import filter_candidates


# Read WhatsApp chat
with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# Preprocess the chat
df = preprocessor.preprocess(data)


# Detect candidate messages
candidates = filter_candidates(df)


print("Total messages:", len(df))
print("Candidate messages:", len(candidates))

print("\n--- Sample Candidates ---")

print(
    candidates[
        ["message_id", "date", "user", "message"]
    ]
    .head(20)
    .to_string(index=False)
)