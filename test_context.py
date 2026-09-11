import preprocessor

from ai.candidate_filter import filter_candidates
from ai.context import get_context


# Read WhatsApp chat
with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# Preprocess
df = preprocessor.preprocess(data)


# Find candidates
candidates = filter_candidates(df)


# Test one candidate
message_id = int(
    candidates.iloc[2]["message_id"]
)


# Get surrounding context
context = get_context(
    df,
    message_id,
    window=2
)


print("\n========== PREVIOUS ==========")

for message in context["previous"]:
    print(
        f'[{message["message_id"]}] '
        f'{message["user"]}: '
        f'{message["message"]}'
    )


print("\n========== CURRENT ==========")

current = context["current"]

print(
    f'[{current["message_id"]}] '
    f'{current["user"]}: '
    f'{current["message"]}'
)


print("\n========== NEXT ==========")

for message in context["next"]:
    print(
        f'[{message["message_id"]}] '
        f'{message["user"]}: '
        f'{message["message"]}'
    )