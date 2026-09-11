def get_context(df, message_id, window=2):
    """
    Get nearby messages around a candidate message.

    Args:
        df: Preprocessed WhatsApp DataFrame.
        message_id: ID of the target message.
        window: Number of messages before and after.

    Returns:
        Dictionary containing previous, current, and next messages.
    """

    # Find the position of the target message
    matching_rows = df.index[
        df["message_id"] == message_id
    ].tolist()

    if not matching_rows:
        raise ValueError(
            f"Message ID {message_id} was not found."
        )

    current_index = matching_rows[0]

    # Calculate context boundaries
    start_index = max(0, current_index - window)
    end_index = min(
        len(df),
        current_index + window + 1
    )

    context_df = df.iloc[start_index:end_index]

    previous_messages = []
    next_messages = []
    current_message = None

    for _, row in context_df.iterrows():

        message = {
            "message_id": int(row["message_id"]),
            "date": str(row["date"]),
            "user": str(row["user"]),
            "message": str(row["message"])
        }

        if row["message_id"] < message_id:
            previous_messages.append(message)

        elif row["message_id"] == message_id:
            current_message = message

        else:
            next_messages.append(message)

    return {
        "previous": previous_messages,
        "current": current_message,
        "next": next_messages
    }