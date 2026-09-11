import preprocessor

from ai.candidate_filter import filter_candidates
from ai.pipeline import analyze_candidates
from ai.postprocessor import validate_ai_results


# Load chat
with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# Preprocess
df = preprocessor.preprocess(data)


# Candidates
candidates = filter_candidates(df)


# --------------------------------------------------
# Create fake AI results
# --------------------------------------------------
# We deliberately add invalid data to verify that
# the postprocessor cleans it correctly.

fake_results = candidates.head(3).copy()

fake_results["is_important"] = [True, False, True]

fake_results["type"] = [
    "task",
    "INVALID_TYPE",
    "request"
]

fake_results["task"] = [
    "Complete assignment",
    "None",
    None
]

fake_results["deadline"] = [
    "tomorrow",
    "null",
    None
]

fake_results["priority"] = [
    "high",
    "INVALID_PRIORITY",
    "medium"
]

fake_results["confidence"] = [
    0.95,
    1.5,
    -0.2
]


# --------------------------------------------------
# Run postprocessor
# --------------------------------------------------

cleaned = validate_ai_results(
    fake_results,
    df
)


print("\n========== CLEANED RESULTS ==========")

print(
    cleaned[
        [
            "message_id",
            "type",
            "task",
            "deadline",
            "priority",
            "confidence"
        ]
    ].to_string(index=False)
)