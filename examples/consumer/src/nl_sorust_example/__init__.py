"""Reuse the installed Sorust binary without copying or rebuilding a kernel."""
from sorust import count_ascii_tokens


def count_prompt_tokens(prompt: str) -> int:
    """Whitespace byte tokens, not a model-specific tokenizer or billing count."""
    return count_ascii_tokens(prompt.encode("utf-8"))
