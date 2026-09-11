import pandas as pd
import preprocessor

from ai.postprocessor import validate_ai_results


# --------------------------------------------------
# Load original WhatsApp chat
# --------------------------------------------------

with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()

df = preprocessor.preprocess(data)


# --------------------------------------------------
# Load previously generated AI results
# --------------------------------------------------

results = pd.read_csv(
    "ai_results.csv"
)


# --------------------------------------------------
# Validate and clean results
# --------------------------------------------------

cleaned_results = validate_ai_results(
    results,
    df
)


# --------------------------------------------------
# Display comparison
# --------------------------------------------------

print(
    "Original AI results:",
    len(results)
)

print(
    "Cleaned AI results:",
    len(cleaned_results)
)


print("\n========== CLEANED RESULTS ==========")

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
            "confidence"
        ]
    ].to_string(index=False)
)