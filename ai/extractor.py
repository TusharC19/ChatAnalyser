import os
import time

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()


class ExtractionResult(BaseModel):
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


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


client = genai.Client(api_key=api_key)


def extract_information(context):
    """
    Analyze a conversation context using Gemini
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

    prompt = f"""
You are a conversation intelligence system analyzing a
WhatsApp conversation.

Your job is to identify actionable or important information.

Understand informal language, Hinglish, abbreviations,
and casual WhatsApp-style conversation.

Do NOT invent information that is not present.

Use the surrounding messages to understand the current message.

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

Return only the requested structured output.
"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
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

            # If this was the final attempt, report the failure.
            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Gemini request failed after "
                    f"{max_retries} attempts: {error}"
                ) from error

            # Wait progressively longer before retrying.
            wait_time = 2 ** attempt

            print(
                f"Gemini request failed. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)