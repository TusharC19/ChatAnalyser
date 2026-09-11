import preprocessor

from ai.candidate_filter import filter_candidates
from ai.pipeline import analyze_candidates
from ai.postprocessor import validate_ai_results


# --------------------------------------------------
# Load WhatsApp chat
# --------------------------------------------------

with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# --------------------------------------------------
# Preprocess chat
# --------------------------------------------------

df = preprocessor.preprocess(data)


# --------------------------------------------------
# Find candidate messages
# --------------------------------------------------

candidates = filter_candidates(df)

print("Total messages:", len(df))
print("Candidates:", len(candidates))


# --------------------------------------------------
# Run AI analysis
# --------------------------------------------------

results = analyze_candidates(
    df,
    candidates,
    window=2,
    batch_size=5,
    delay=1,
    max_batches=9
)


print(
    "\nAI results before post-processing:",
    len(results)
)


# --------------------------------------------------
# Validate and clean AI results
# --------------------------------------------------

cleaned_results = validate_ai_results(
    results,
    df
)


print(
    "AI results after post-processing:",
    len(cleaned_results)
)

cleaned_results.to_csv(
    "ai_results.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nAI results saved to ai_results.csv")

# --------------------------------------------------
# Display final results
# --------------------------------------------------

print("\n========== FINAL CLEAN RESULTS ==========")

print(
    cleaned_results[
        [
            "message_id",
            "user",
            "message",
            "type",
            "task",
            "deadline",
            "priority",
            "confidence",
            "evidence"
        ]
    ].to_string(index=False)
)