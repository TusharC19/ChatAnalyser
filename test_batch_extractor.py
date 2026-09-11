import preprocessor

from ai.candidate_filter import filter_candidates
from ai.pipeline import create_batches
from ai.extractor import extract_batch_information


# Load WhatsApp chat
with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# Preprocess chat
df = preprocessor.preprocess(data)


# Find candidate messages
candidates = filter_candidates(df)


# Create batches
batches = create_batches(
    df,
    candidates,
    batch_size=5,
    window=2
)

# Test batch 8
batch = batches[7]

print("Testing batch with message IDs:")

for item in batch:
    print(item["message_id"])


# Send ONE batch to Gemini
result = extract_batch_information(batch)


# Display results
print("\n========== BATCH AI RESULT ==========")

for item in result.results:

    print(f"\nMessage ID: {item.message_id}")
    print(f"Important: {item.is_important}")
    print(f"Type: {item.type}")
    print(f"Task: {item.task}")
    print(f"Deadline: {item.deadline}")
    print(f"Priority: {item.priority}")
    print(f"Confidence: {item.confidence}")
    print(f"Evidence: {item.evidence}")