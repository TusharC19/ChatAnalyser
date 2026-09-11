import preprocessor

from ai.candidate_filter import filter_candidates
from ai.pipeline import analyze_candidates


with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


df = preprocessor.preprocess(data)

candidates = filter_candidates(df).head(3)

print("Total messages:", len(df))
print("Candidate messages:", len(candidates))


results = analyze_candidates(
    df,
    candidates,
    window=2,
    delay=1
)


print("\n========== FINAL RESULTS ==========")

print(
    results[
        [
            "message_id",
            "user",
            "message",
            "type",
            "task",
            "deadline",
            "priority",
            "confidence"
        ]
    ].to_string(index=False)
)