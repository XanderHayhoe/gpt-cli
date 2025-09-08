from __future__ import annotations
import os, subprocess
import typer
from rich import print
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.console import Group
import typing as t

from gpt_cli.config import get_config, save_config
from gpt_cli.llm import get_command
from gpt_cli.models import OpenAIModel

app = typer.Typer(
    add_completion=False,
    help="AI-powered command helper (MVP)",
    no_args_is_help=True,
)

config_app = typer.Typer(
    help="Manage the configuration for gpt-cli.",
    no_args_is_help=True,
)
app.add_typer(config_app, name="config")

@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="The configuration key to set."),
    value: str = typer.Argument(..., help="The value to set for the key."),
):
    """
    Set a configuration value.
    """
    config = get_config()
    config[key] = value
    save_config(config)
    print(f"Set {key} to {value}")

@config_app.command("get")
def config_get(
    key: t.Optional[str] = typer.Argument(None, help="The configuration key to get."),
):
    """
    Get a configuration value.
    """
    config = get_config()
    if key:
        print(config.get(key))
    else:
        print(config)

@app.callback()
def main():
    """
    AI-powered command helper.
    """
    pass

@app.command("ask")
def ask(
    request: str,
    model: OpenAIModel = typer.Option(
        None,
        "--model",
        "-m",
        help="The OpenAI model to use for the request.",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        help="The OpenAI API key to use for the request.",
    ),
):
    
    """
    Propose a command for your natural-language request.
    """
    
    payload = get_command(request, model=model, api_key=api_key)

    blocks = [
        Markdown("**Rationale**\n\n" + payload["rationale"]),
        Markdown("**Warnings**\n\n- " + "\n- ".join(payload["warnings"])),
        Panel(Syntax(payload["command"], "bash", word_wrap=True), title="Proposed command"),
    ]

    print(Panel(Group(*blocks), title="gpt-cli"))
@app.command("mode")
def mode(
    request_type: str = typer.Argument(..., help="select the type of requests you want (cli, programmer, file assistant, custom)"),
    custom_prompt: t.Optional[str] = typer.Option(None, "--custom-prompt", help="A custom prompt to use."),
    file_location: t.Optional[str] = typer.Option(None, "--file-location", help="Path to a file containing a custom prompt."),
):
    """
    # set the type of requests you want
    options:
    -cli
    -programmer
    -file assistant
    -custom: this custom mode allows you to set your own prompt for the AI to follow. 
        You can specify the prompt in a separate file and provide the file path as an argument.
    """
    
    pass

if __name__ == "__main__":
    app()
