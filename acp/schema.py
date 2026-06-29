"""
ACP Schema Stubs - Compatibility module for ACP adapter.

This module provides stub classes for ACP schema types that the
acp_adapter expects but are not available in the installed acp_sdk package.

These are simplified stubs for testing purposes.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class AuthMethodAgent(BaseModel):
    """Agent-managed authentication method."""
    id: str
    name: str
    description: str
    provider: Optional[str] = None


class TerminalAuthMethod(BaseModel):
    """Terminal setup authentication method."""
    id: str = "terminal-setup"
    name: str = "Terminal Setup"
    description: str = "Configure credentials via terminal"


class ToolCallUpdate(BaseModel):
    """Tool call update payload for ACP."""
    tool_name: str
    path: str
    old_text: str
    new_text: str
    arguments: Dict[str, Any]


# Add other commonly used ACP schema stubs here as needed
