import re


# Strong action phrases.
# Includes common English + Hinglish/WhatsApp expressions.
ACTION_PATTERNS = [
    r"\b(submit|complete|finish|prepare|create|make|update|fix|review|fill|solve|send|share)\b",

    r"\b(bhar de|bhar do|bhej de|bhej do|bhej dena|send kar|share kar)\b",

    r"\b(check kar|check karke|bata dena|bata do|bata de|pta krke|pata karke)\b",

    r"\b(kar dena|kar do|kar de|kr dena|kr do|kr de|karke bhej)\b",

    r"\b(ans bhej|answer bhej|questions solve|form bhar)\b",
]


# Requests.
REQUEST_PATTERNS = [
    r"\b(can you|could you|would you|please|pls|plz)\b",
    r"\b(mujhe.*bhej|mujhe.*chahiye)\b",
    r"\b(ek baar.*bata|ek bar.*bata)\b",
]


# Deadline / time-related signals.
DEADLINE_PATTERNS = [
    r"\b(today|tomorrow|tonight|morning|evening)\b",
    r"\b(aaj|kal|raat|subah|shaam)\b",
    r"\b(deadline|due|before|within|by)\b",
    r"\b(baje|bje)\b",
    r"\b(submit.*\d+|assignment.*\d+)\b",

    # Dates such as 1st, 2nd, 10th etc.
    r"\b\d{1,2}(st|nd|rd|th)\b",
]


# Decision-related signals.
DECISION_PATTERNS = [
    r"\b(decide|decided|decision|final|finalized|choose|selected|agreed)\b",
    r"\b(decide kar|decide kr|final kar|select kar)\b",
    r"\b(we will|we'll|lets|let's)\b",
]


# Obvious messages that should never go to the AI.
NOISE_PATTERNS = [
    r"^(ok|okay|okk|k|kk|yes|no|haan|ha|hmm|hm|lol|haha|hehe)$",
    r"^(good morning|good night|gn|gm)$",
    r"^[😂🤣😭❤️👍🙏😊😅🙂🙃]+$",
]


def _contains_pattern(message, patterns):
    """Return True if any pattern matches."""
    return any(
        re.search(pattern, message, flags=re.IGNORECASE)
        for pattern in patterns
    )


def calculate_candidate_score(message):
    """
    Calculate how likely a message is to contain
    actionable information.
    """

    if not isinstance(message, str):
        return 0, []

    message = message.strip().lower()

    if not message:
        return 0, []

    # Very short conversational messages are usually noise.
    if len(message.split()) <= 1:
        return 0, []

    # Obvious noise.
    for pattern in NOISE_PATTERNS:
        if re.fullmatch(pattern, message):
            return 0, []

    # URLs alone are not enough to make a message actionable.
    text_without_urls = re.sub(
        r"https?://\S+|www\.\S+",
        "",
        message
    ).strip()

    if not text_without_urls:
        return 0, []

    score = 0
    reasons = []

    if _contains_pattern(message, ACTION_PATTERNS):
        score += 3
        reasons.append("action")

    if _contains_pattern(message, REQUEST_PATTERNS):
        score += 2
        reasons.append("request")

    if _contains_pattern(message, DEADLINE_PATTERNS):
        score += 3
        reasons.append("deadline")

    if _contains_pattern(message, DECISION_PATTERNS):
        score += 2
        reasons.append("decision")

    # A question by itself is weak evidence.
    if "?" in message:
        score += 1
        reasons.append("question")

    return score, reasons


def is_candidate(message):
    """
    Return True when a message has enough evidence
    to be sent for further AI analysis.
    """

    score, _ = calculate_candidate_score(message)

    # Conservative threshold.
    return score >= 3


def filter_candidates(df):
    """
    Filter the DataFrame and attach candidate metadata.
    """

    result = df.copy()

    scores = []
    reasons = []

    for message in result["message"]:
        score, reason = calculate_candidate_score(message)
        scores.append(score)
        reasons.append(", ".join(reason))

    result["candidate_score"] = scores
    result["candidate_reason"] = reasons
    result["is_candidate"] = result["candidate_score"] >= 3

    # Remove WhatsApp system/group notifications.
    candidates = result[
        (result["is_candidate"])
        & (result["user"] != "group_notification")
    ].copy()

    return candidates