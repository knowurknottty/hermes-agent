"""
ACP Schema Stubs - Import compatibility fix for the ACP adapter.

This is NOT an ACP protocol implementation. It provides stub classes that
fix import errors when the installed acp_sdk package lacks schema types.
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
