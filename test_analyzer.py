import preprocessor

from ai.analyzer import analyze_chat


# --------------------------------------------------
# Load WhatsApp chat
# --------------------------------------------------

with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# --------------------------------------------------
# Preprocess chat
# --------------------------------------------------

df = preprocessor.preprocess(data)

print("Total messages:", len(df))


# --------------------------------------------------
# Run complete AI analysis
# --------------------------------------------------

print("\nRunning AI conversation analysis...")

ai_results = analyze_chat(
    df,
    window=2,
    batch_size=5,
    delay=1
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print(
    "\nAI results:",
    len(ai_results)
)

print(
    "\nColumns:"
)

print(
    ai_results.columns.tolist()
)


print(
    "\n========== SAMPLE RESULTS =========="
)

print(
    ai_results[
        [
            "message_id",
            "type",
            "task",
            "deadline",
            "priority",
            "confidence",
            "evidence"
        ]
    ].head(10).to_string(index=False)
)