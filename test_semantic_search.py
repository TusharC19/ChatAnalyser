import pandas as pd

import preprocessor
from ai.semantic_search import SemanticSearch


# =========================
# LOAD CHAT
# =========================

with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


df = preprocessor.preprocess(data)

print("Total messages:", len(df))


# =========================
# LOAD AI RESULTS
# =========================

ai_results = None

try:
    ai_results = pd.read_csv(
        "ai_results.csv"
    )

    print(
        "AI results loaded:",
        len(ai_results)
    )

except FileNotFoundError:

    print(
        "ai_results.csv not found. "
        "Continuing without AI results."
    )


# =========================
# BUILD SEARCH INDEX
# =========================

search = SemanticSearch()

print("\nBuilding semantic index...")

search.build_index(
    df,
    ai_results=ai_results
)

print(
    "Semantic index built successfully."
)


# =========================
# SEARCH
# =========================

query = (
    "When do I need to submit "
    "the assignment?"
)

print(
    f"\nSearching for: {query}"
)

results = search.search(
    query,
    top_k=5
)


# =========================
# DISPLAY RESULTS
# =========================

print(
    "\n========== SEARCH RESULTS =========="
)


for result in results:

    print(
        f"\nMessage ID: "
        f"{result['message_id']}"
    )

    print(
        f"Semantic score: "
        f"{result['semantic_score']:.4f}"
    )

    print(
        f"Keyword score: "
        f"{result['keyword_score']:.4f}"
    )

    print(
        f"AI score: "
        f"{result['ai_score']:.4f}"
    )

    print(
        f"Combined score: "
        f"{result['score']:.4f}"
    )

    print(
        f"\nMatched message: "
        f"{result['user']}: "
        f"{result['message']}"
    )


    # =========================
    # AI INSIGHT
    # =========================

    ai_result = result["ai_result"]

    if ai_result is not None:

        print("\nAI Insight:")

        print(
            f"Type: "
            f"{ai_result['type']}"
        )

        print(
            f"Task: "
            f"{ai_result['task']}"
        )

        print(
            f"Deadline: "
            f"{ai_result['deadline']}"
        )

        print(
            f"Priority: "
            f"{ai_result['priority']}"
        )

        print(
            f"Confidence: "
            f"{ai_result['confidence']}"
        )

        print(
            f"Evidence: "
            f"{ai_result['evidence']}"
        )


    # =========================
    # CONTEXT
    # =========================

    print("\nContext:")

    for message in result["context"]:

        print(
            f"[{message['message_id']}] "
            f"{message['user']}: "
            f"{message['message']}"
        )

    print(
        "\n" + "-" * 60
    )