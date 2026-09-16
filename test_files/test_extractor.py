import preprocessor

from ai.candidate_filter import filter_candidates
from ai.context import get_context
from ai.extractor import extract_information


# Read chat
with open("chat.txt", "r", encoding="utf-8") as f:
    data = f.read()


# Preprocess
df = preprocessor.preprocess(data)


# Find candidates
candidates = filter_candidates(df)


# Pick a strong real candidate
message_id = 575


# Get surrounding context
context = get_context(
    df,
    message_id,
    window=2
)


print("\n========== CONTEXT ==========")

for message in context["previous"]:
    print(
        f'[{message["message_id"]}] '
        f'{message["user"]}: '
        f'{message["message"]}'
    )

current = context["current"]

print(
    f'\n[{current["message_id"]}] '
    f'{current["user"]}: '
    f'{current["message"]}'
)

for message in context["next"]:
    print(
        f'[{message["message_id"]}] '
        f'{message["user"]}: '
        f'{message["message"]}'
    )


# Send context to Gemini
result = extract_information(context)


print("\n========== AI RESULT ==========")

print(result.model_dump_json(indent=2))