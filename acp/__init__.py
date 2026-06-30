"""
ACP Import Compatibility Fix - Stub classes for ACP schema types.

This is NOT an ACP protocol implementation. It provides stub classes that
fix import errors when the installed acp_sdk package lacks schema types.
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
