from __future__ import annotations
from enum import Enum

class OpenAIModel(str, Enum):
    GPT5 = "gpt-5"
    GPT5_MINI = "gpt-5-mini"
    GPT5_NANO = "gpt-5-nano"
    GPT4 = "gpt-4.1"
