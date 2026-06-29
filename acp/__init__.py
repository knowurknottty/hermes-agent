"""
ACP Protocol - Compatibility stubs.

This package provides stub modules for ACP schema types
that the hermes-agent ACP adapter expects.
"""

from .schema import (
    AuthMethodAgent,
    TerminalAuthMethod,
    ToolCallUpdate,
)

__all__ = [
    "AuthMethodAgent",
    "TerminalAuthMethod",
    "ToolCallUpdate",
]
