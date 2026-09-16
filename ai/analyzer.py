from ai.candidate_filter import filter_candidates
from ai.pipeline import analyze_candidates
from ai.postprocessor import validate_ai_results


def analyze_chat(
    df,
    window=2,
    batch_size=5,
    delay=1
):
    """
    Run the complete AI conversation analysis pipeline.

    Flow:
        DataFrame
            ↓
        Candidate Filtering
            ↓
        Gemini Analysis
            ↓
        Post-processing
            ↓
        Clean AI Results
    """

    # -----------------------------------------
    # 1. Find candidate messages
    # -----------------------------------------

    candidates = filter_candidates(df)

    if candidates.empty:
        return candidates

    # -----------------------------------------
    # 2. Run AI analysis
    # -----------------------------------------

    results = analyze_candidates(
        df,
        candidates,
        window=window,
        batch_size=batch_size,
        delay=delay
    )

    if results.empty:
        return results

    # -----------------------------------------
    # 3. Validate AI results
    # -----------------------------------------

    cleaned_results = validate_ai_results(
        results,
        df
    )

    return cleaned_results