from __future__ import annotations
import json
from pathlib import Path
from typing import TypedDict

from gpt_cli.models import OpenAIModel


class GptCliConfig(TypedDict):
    api_key: str | None
    model: str


DEFAULT_CONFIG: GptCliConfig = {
    "api_key": None,
    "model": OpenAIModel.GPT5.value,
}

CONFIG_FILE = Path.home() / ".gpt-cli-config.json"


def get_config() -> GptCliConfig:
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(config: GptCliConfig):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
