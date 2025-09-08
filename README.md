# gpt-cli

An AI-powered command-line helper that uses OpenAI's models to suggest shell commands based on natural language requests.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd gpt-cli
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

## Configuration

Before using `gpt-cli`, you need to configure your OpenAI API key. You can also set a default model to use for your requests.

### Set API Key

Set your OpenAI API key using the `config set` command:

```bash
gpt-cli config set api_key "your-api-key-here"