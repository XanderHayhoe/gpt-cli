from __future__ import annotations
import os
import openai

from gpt_cli.config import get_config
from gpt_cli.models import OpenAIModel


def get_command(request: str, model: OpenAIModel | None = None, api_key: str | None = None) -> dict:
    """
    Calls the OpenAI API to get a command suggestion.
    """
    config = get_config()
    api_key = api_key or config.get("api_key") or os.environ.get("OPENAI_API_KEY")
    model = model or config.get("model")

    if not api_key:
        return {
            "command": "echo 'Error: OPENAI_API_KEY not set.'",
            "rationale": "The OpenAI API key is required. You can set it with `gpt-cli config set api_key YOUR_KEY` or the OPENAI_API_KEY environment variable.",
            "warnings": [],
        }

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI assistant that suggests shell commands. The user will provide a natural language request, and you will provide a single, executable shell command.
Respond with a JSON object with three keys:
1. `command`: The suggested shell command as a string.
2. `rationale`: A brief explanation of why you are suggesting this command.
3. `warnings`: A list of strings of any potential warnings or dangers (e.g., "this command can delete files"). If there are no warnings, provide an empty list.
Only output the JSON object.
                    """,
                },
                {"role": "user", "content": request},
            ],
            response_format={"type": "json_object"},
        )
        payload = response.choices[0].message.content
        import json
        return json.loads(payload)
    except Exception as e:
        return {
            "command": f"echo 'Error: {e}'",
            "rationale": "An error occurred while communicating with the OpenAI API.",
            "warnings": [str(e)],
        }
