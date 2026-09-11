import preprocessor

from ai.candidate_filter import filter_candidates
from ai.pipeline import create_batches


with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


df = preprocessor.preprocess(data)

candidates = filter_candidates(df)

batches = create_batches(
    df,
    candidates,
    batch_size=5,
    window=2
)


print("Total messages:", len(df))
print("Candidates:", len(candidates))
print("Batches:", len(batches))


print("\n========== BATCHES ==========")

for index, batch in enumerate(batches, start=1):

    message_ids = [
        item["message_id"]
        for item in batch
    ]

    print(
        f"Batch {index}: "
        f"{len(batch)} candidates → "
        f"{message_ids}"
    )