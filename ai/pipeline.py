import time
import pandas as pd

from ai.context import get_context
from ai.extractor import extract_batch_information


def create_batches(df, candidates, batch_size=5, window=2):
    """
    Prepare candidate conversations into batches.

    This function does NOT call Gemini.
    It only groups candidate contexts for later batch processing.
    """

    items = []

    for _, candidate in candidates.iterrows():

        message_id = int(candidate["message_id"])

        context = get_context(
            df,
            message_id,
            window=window
        )

        items.append({
            "message_id": message_id,
            "context": context
        })

    batches = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batches.append(batch)

    return batches


def analyze_candidates(
    df,
    candidates,
    window=2,
    batch_size=5,
    delay=1,
    max_batches=None
):
    """
    Analyze candidate messages using batched Gemini requests.
    """

    batches = create_batches(
        df,
        candidates,
        batch_size=batch_size,
        window=window
    )

    if max_batches is not None:
        batches = batches[:max_batches]

    results = []

    total_batches = len(batches)

    for batch_index, batch in enumerate(
        batches,
        start=1
    ):

        message_ids = [
            item["message_id"]
            for item in batch
        ]

        print(
            f"Analyzing batch "
            f"{batch_index}/{total_batches} "
            f"(message_ids={message_ids})"
        )

        try:

            ai_results = extract_batch_information(
                batch
            )

            ai_results_by_id = {
                result.message_id: result
                for result in ai_results.results
            }

            for item in batch:

                message_id = item["message_id"]

                candidate_row = candidates[
                    candidates["message_id"] == message_id
                ].iloc[0]

                ai_result = ai_results_by_id.get(
                    message_id
                )

                if ai_result is None:

                    print(
                        f"Warning: Gemini did not return "
                        f"a result for message {message_id}"
                    )

                    continue

                results.append({
                    "message_id": message_id,
                    "date": candidate_row["date"],
                    "user": candidate_row["user"],
                    "message": candidate_row["message"],
                    "candidate_score": candidate_row[
                        "candidate_score"
                    ],
                    "candidate_reason": candidate_row[
                        "candidate_reason"
                    ],

                    "is_important": ai_result.is_important,
                    "type": ai_result.type,
                    "task": ai_result.task,
                    "deadline": ai_result.deadline,
                    "priority": ai_result.priority,
                    "confidence": ai_result.confidence,
                    "evidence": ai_result.evidence,
                })

        except Exception as error:

            print(
                f"Failed to analyze batch "
                f"{batch_index}: {error}"
            )

        if batch_index < total_batches:
            time.sleep(delay)

    return pd.DataFrame(results)