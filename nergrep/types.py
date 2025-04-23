"""Type definitions for the nergrep package."""

from dataclasses import dataclass

@dataclass
class EntityRecord:
    """Record of an extracted named entity."""
    text: str
    label: str
    sentence: str
    start: int
    end: int 