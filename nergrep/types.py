"""Type definitions for the nergrep package."""

from dataclasses import dataclass


@dataclass
class EntityRecord:
    """Record of an extracted named entity.

    Attributes:
        text: The actual text of the entity
        label: The entity type label (e.g., 'PERSON', 'ORG', 'GPE')
        sentence: The full sentence containing the entity
        start: Character position where the entity starts
        end: Character position where the entity ends
    """
    text: str
    label: str
    sentence: str
    start: int
    end: int
