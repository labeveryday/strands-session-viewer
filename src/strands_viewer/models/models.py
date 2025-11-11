"""Model configurations for Session Analyzer."""

import os
from dotenv import load_dotenv

try:
    from strands.models.anthropic import AnthropicModel
    from strands.models.openai import OpenAIModel
    from strands.models.ollama import OllamaModel

    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    AnthropicModel = None
    OpenAIModel = None
    OllamaModel = None


# Load environment variables
load_dotenv()


# ============================================================================
# ANTHROPIC MODEL
# https://docs.claude.com/en/docs/about-claude/models/overview
# ============================================================================


def anthropic_model(
    api_key: str = os.getenv("ANTHROPIC_API_KEY"),
    model_id: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 4000,
    temperature: float = 1,
    thinking: bool = True,
    budget_tokens: int = 1024,
) -> "AnthropicModel":
    """
    Create an Anthropic model instance.

    Args:
        api_key: The API key to use (default: os.getenv("ANTHROPIC_API_KEY"))
        model_id: The model ID to use (default: claude-haiku-4-5-20251001)
        max_tokens: The maximum number of tokens to generate (default: 4000, max: 64000)
        temperature: The temperature to use (default: 1)
        thinking: Whether to use extended thinking (default: True)
        budget_tokens: The budget tokens for thinking (default: 1024)

    Returns:
        AnthropicModel instance

    Available models:
        - claude-haiku-4-5-20251001 - 200k context, 64k max_output
        - claude-sonnet-4-5-20250929 - 200k context (1M beta), 64k max_output
        - claude-sonnet-4-20250514 - 200k context (1M beta), 64k max_output
        - claude-3-7-sonnet-20250219 - 200k context, 64k max_output
        - claude-3-5-haiku-20241022 - 200k context, 8k max_output
    """
    if not MODELS_AVAILABLE:
        raise ImportError(
            "Strands models not available. Install with: pip install strands-session-viewer[ai]"
        )

    if thinking:
        if budget_tokens >= max_tokens:
            raise ValueError("Budget tokens cannot be greater than max tokens")
        thinking_config = {"type": "enabled", "budget_tokens": budget_tokens}
    else:
        thinking_config = {"type": "disabled"}

    return AnthropicModel(
        client_args={
            "api_key": api_key,
        },
        max_tokens=max_tokens,
        model_id=model_id,
        params={"temperature": temperature, "thinking": thinking_config},
    )


# ============================================================================
# OPENAI MODEL
# https://platform.openai.com/docs/models
# ============================================================================


def openai_model(
    api_key: str = os.getenv("OPENAI_API_KEY"),
    model_id: str = "gpt-5-mini-2025-08-07",
    max_tokens: int = 16000,
    temperature: float = 1,
    reasoning_effort: str = "medium",
) -> "OpenAIModel":
    """
    Create an OpenAI model instance.

    Args:
        api_key: The API key to use (default: os.getenv("OPENAI_API_KEY"))
        model_id: The model ID to use (default: gpt-5-mini-2025-08-07)
        max_tokens: The maximum number of tokens to generate (default: 16000, max: 128000)
        temperature: The temperature to use (default: 1)
        reasoning_effort: The reasoning effort to use (default: "medium")

    Returns:
        OpenAIModel instance

    Available models:
        - gpt-5-2025-08-07 - 400k context, 128K max_output
        - gpt-4.1-2025-04-14 - 1M context, 32K max_output
        - o4-mini-2025-04-16 - 200k context, 100k max_output
        - gpt-5-mini-2025-08-07 - 400k context, 128K max_output
        - gpt-5-nano-2025-08-07 - 400k context, 128K max_output
        - gpt-4o-2024-11-20 - 128k context, 16k max_output
        - gpt-5-pro-2025-10-06 - 400k context, 272K max_output
        - o4-mini-deep-research-2025-06-26 - 200k context, 100k max_output
    """
    if not MODELS_AVAILABLE:
        raise ImportError(
            "Strands models not available. Install with: pip install strands-session-viewer[ai]"
        )

    return OpenAIModel(
        client_args={
            "api_key": api_key,
        },
        model_id=model_id,
        params={
            "max_completion_tokens": max_tokens,
            "temperature": temperature,
            "reasoning_effort": reasoning_effort,
        },
    )


# ============================================================================
# OLLAMA MODEL
# https://ollama.com/library
# ============================================================================


def ollama_model(
    host: str = os.getenv("OLLAMA_HOST"),
    model_id: str = "qwen3:4b",
    max_tokens: int = 2000,
    temperature: float = 1,
) -> "OllamaModel":
    """
    Create an Ollama model instance.

    Args:
        host: The host to use (default: os.getenv("OLLAMA_HOST"))
        model_id: The model ID to use (default: qwen3:4b)
        max_tokens: The maximum number of tokens to generate (default: 2000, max: 128000)
        temperature: The temperature to use (default: 1)

    Returns:
        OllamaModel instance

    Available models:
        - qwen3:4b - 260k context, 128K max_output
        - llama3.1:latest - 131k context, 128K max_output
        - gemma3n:e4b - 32k context, 8K max_output (does not support tools)
        - nomic-embed-text:latest - 2k context (embedding model)
    """
    if not MODELS_AVAILABLE:
        raise ImportError(
            "Strands models not available. Install with: pip install strands-session-viewer[ai]"
        )

    if model_id == "qwen3:4b":
        max_tokens = 128000
    elif model_id == "llama3.1:latest":
        max_tokens = 128000
    elif model_id == "gemma3n:e4b":
        max_tokens = 8000
    else:
        raise ValueError(f"Model ID {model_id} not supported")

    if model_id == "gemma3n:e4b":
        print("NOTE: Tools are not supported with this model.")

    return OllamaModel(
        host=host,
        model_id=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
    )
