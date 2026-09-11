import os
import re
import time

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()


class ExtractionResult(BaseModel):
    message_id: int = Field(
        description="The message_id of the candidate conversation being analyzed."
    )

    is_important: bool = Field(
        description="Whether this conversation contains useful actionable information."
    )

    type: str = Field(
        description="One of: task, request, deadline, decision, information, none."
    )

    task: str | None = Field(
        default=None,
        description="The action that needs to be performed, if any."
    )

    deadline: str | None = Field(
        default=None,
        description="Deadline or relevant time mentioned in the conversation, if any."
    )

    priority: str = Field(
        description="One of: low, medium, high."
    )

    confidence: float = Field(
        description="Confidence from 0.0 to 1.0."
    )

    evidence: str | None = Field(
        default=None,
        description=(
            "The exact message text or short phrase from the "
            "conversation that supports the classification. "
            "Use null when there is no sufficient evidence."
        )
    )


class BatchExtractionResult(BaseModel):
    results: list[ExtractionResult]


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


client = genai.Client(api_key=api_key)


def extract_information(context):
    """
    Analyze a single conversation context using Gemini
    and return structured information.
    """

    previous_messages = context["previous"]
    current_message = context["current"]
    next_messages = context["next"]

    previous_text = "\n".join(
        f'{msg["user"]}: {msg["message"]}'
        for msg in previous_messages
    )

    next_text = "\n".join(
        f'{msg["user"]}: {msg["message"]}'
        for msg in next_messages
    )

    current_text = (
        f'{current_message["user"]}: '
        f'{current_message["message"]}'
    )

    message_id = current_message["message_id"]

    prompt = f"""
You are a conversation intelligence system analyzing a
WhatsApp conversation.

Your job is to identify actionable or important information.

Understand informal language, Hinglish, abbreviations,
and casual WhatsApp-style conversation.

Do NOT invent information that is not present.

Use the surrounding messages to understand the current message.

MESSAGE_ID:
{message_id}

PREVIOUS MESSAGES:
{previous_text}

CURRENT MESSAGE:
{current_text}

NEXT MESSAGES:
{next_text}

Classify the conversation into one of:

- task
- request
- deadline
- decision
- information
- none

If there is an actionable task, describe it briefly.

If a deadline or time is mentioned, extract it.
Otherwise use null.

Use:
- high priority for urgent/deadline-sensitive items
- medium for useful requests/tasks
- low for less important information

If the context is insufficient, do not guess.
Use lower confidence.

IMPORTANT:
Return the MESSAGE_ID exactly as provided.

Return only the requested structured output.
"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ExtractionResult,
                },
            )

            return ExtractionResult.model_validate_json(
                response.text
            )

        except Exception as error:

            error_text = str(error)

            # Handle Gemini rate-limit errors.
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                retry_match = re.search(
                    r"retryDelay.*?(\d+)",
                    error_text
                )

                if retry_match:
                    wait_time = int(retry_match.group(1)) + 1
                else:
                    wait_time = 60

                if attempt == max_retries - 1:
                    raise RuntimeError(
                        "Gemini rate limit exceeded. "
                        f"Please wait before trying again: {error}"
                    ) from error

                print(
                    f"Gemini rate limit reached. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            # Other temporary errors.
            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Gemini request failed after "
                    f"{max_retries} attempts: {error}"
                ) from error

            wait_time = 2 ** attempt

            print(
                f"Gemini request failed. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


def extract_batch_information(batch):
    """
    Analyze multiple candidate conversations
    using a single Gemini request.
    """

    conversation_blocks = []

    for item in batch:

        message_id = item["message_id"]
        context = item["context"]

        previous_text = "\n".join(
            f'{msg["user"]}: {msg["message"]}'
            for msg in context["previous"]
        )

        current = context["current"]

        current_text = (
            f'{current["user"]}: '
            f'{current["message"]}'
        )

        next_text = "\n".join(
            f'{msg["user"]}: {msg["message"]}'
            for msg in context["next"]
        )

        conversation = f"""
MESSAGE_ID: {message_id}

PREVIOUS MESSAGES:
{previous_text}

CURRENT MESSAGE:
{current_text}

NEXT MESSAGES:
{next_text}
"""

        conversation_blocks.append(conversation)

    all_conversations = "\n\n--------------------\n\n".join(
        conversation_blocks
    )

    prompt = f"""

You are a conversation intelligence system analyzing
multiple WhatsApp conversations.

Analyze EACH conversation independently.

Your goal is to identify genuinely useful information
from the conversation, especially tasks, requests,
deadlines, decisions, and important updates.

Understand:
- informal WhatsApp language
- Hinglish
- abbreviations
- spelling mistakes
- casual conversation

STRICT ACCURACY RULES:

1. DO NOT INVENT INFORMATION.
   Only use information explicitly present in the
   conversation or clearly established by its surrounding
   messages.

2. DO NOT ASSUME WHAT A VAGUE MESSAGE REFERS TO.
   For example, if someone only says "kal raat ko",
   do not invent what they will do unless the surrounding
   conversation clearly establishes the action.

3. A TASK means there is a clear action that someone
   needs to perform.

4. A REQUEST means someone is clearly asking another
   person for something.

5. A DEADLINE means a specific date, day, time, or
   time constraint is explicitly mentioned AND the
   surrounding conversation clearly establishes what
   it applies to.

6. An INFORMATION message contains a useful fact,
   update, announcement, or knowledge that does not
   necessarily require an action.

7. A DECISION means the conversation clearly indicates
   that something has been decided, finalized, selected,
   or agreed upon.

8. Use NONE when:
   - the message is casual conversation
   - the context is insufficient
   - the message is too vague to classify reliably
   - there is no genuinely useful information

9. If you are uncertain, prefer NONE or INFORMATION
   rather than making an unsupported assumption.

10. The TASK field must describe only an action that is
    actually supported by the conversation.

11. The DEADLINE field must contain only a time/date
    explicitly supported by the conversation.
    Do not create a deadline from assumptions.

12. is_important should be TRUE only when the
    conversation contains genuinely useful information,
    an actionable request/task, a meaningful deadline,
    or a clear decision.

13. Preserve the MESSAGE_ID exactly as provided.

15. EVIDENCE REQUIREMENT:
    For every result that is not NONE, provide an
    "evidence" field containing the exact original
    message text or a short exact phrase from the
    conversation that directly supports your decision.

16. Do NOT write an explanation in the evidence field.
    Evidence must come directly from the conversation.

17. If there is no clear supporting evidence, use:
    - type = none
    - task = null
    - deadline = null
    - evidence = null

18. For tasks, the evidence must support the actual action
    described in the task.

19. For deadlines, the evidence must support both the
    existence of the deadline and what it applies to.

20. Do not use surrounding context to invent an action.
    Context may clarify a message, but the resulting task
    must still be directly supported by the conversation.

CONVERSATIONS:


{all_conversations}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": BatchExtractionResult,
        },
    )

    return BatchExtractionResult.model_validate_json(
        response.text
    )