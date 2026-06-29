"""
ACP Compatibility Module - Stub classes for ACP schema types.

This module provides stub classes for ACP schema types that the
hermes-agent ACP adapter expects but are not available in the
installed acp_sdk package.

These are simplified stubs for testing and compatibility purposes.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class AuthMethodAgent(BaseModel):
    """Agent-managed authentication method."""
    id: str
    name: str
    description: str
    provider: Optional[str] = None
    type: Optional[str] = None  # Add type field expected by tests


class TerminalAuthMethod(BaseModel):
    """Terminal setup authentication method."""
    id: str = "terminal-setup"
    name: str = "Terminal Setup"
    description: str = "Configure credentials via terminal"
    type: str = "terminal"  # Add type field with default value
    args: list[str] = ["--setup"]  # Add args field expected by tests


class ToolCallUpdate(BaseModel):
    """Tool call update payload for ACP."""
    tool_call_id: str
    title: str
    kind: str
    status: str
    content: list[Any]  # List of diff content objects
    rawInput: Dict[str, Any]


class ToolDiffContent(BaseModel):
    """Diff content for ACP tool calls."""
    path: str
    oldText: Optional[str] = None  # Allow None for new files
    newText: Optional[str] = None  # Allow None for deleted files


class PermissionOption(BaseModel):
    """Permission option for ACP approval dialog."""
    option_id: str
    kind: str
    name: str


# Export commonly used ACP schema stubs
__all__ = [
    "AuthMethodAgent",
    "TerminalAuthMethod",
    "ToolCallUpdate",
    "PermissionOption",
]
