"""Entity filtering functionality."""

import re
from dataclasses import dataclass
from typing import List, Optional, Set

from rapidfuzz import fuzz

from .types import EntityRecord

# Type alias to reduce line length
EntityList = List[EntityRecord]

@dataclass
class FilterConfig:
    """Configuration for entity filtering."""
    entity_types: Optional[Set[str]] = None
    blacklist: Optional[Set[str]] = None
    whitelist: Optional[Set[str]] = None
    fuzzy_match: Optional[str] = None
    fuzzy_threshold: float = 80.0
    regex_pattern: Optional[str] = None
    partial_word: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None

def filter_by_type(
    entities: EntityList,
    allowed_types: Set[str]
) -> EntityList:
    """Filter entities by their type.

    Args:
        entities: List of EntityRecord instances
        allowed_types: Set of allowed entity types

    Returns:
        Filtered list of entities
    """
    return [
        entity for entity in entities
        if entity.label in allowed_types
    ]

def filter_by_blacklist(
    entities: EntityList,
    blacklist: Set[str]
) -> EntityList:
    """Filter out entities that appear in the blacklist.

    Args:
        entities: List of EntityRecord instances
        blacklist: Set of terms to exclude

    Returns:
        Filtered list of entities
    """
    return [
        entity for entity in entities
        if entity.text.lower() not in {word.lower() for word in blacklist}
    ]

def filter_by_whitelist(
    entities: EntityList,
    whitelist: Set[str]
) -> EntityList:
    """Filter entities to only include those that appear in the whitelist.

    Args:
        entities: List of EntityRecord instances
        whitelist: Set of terms to include

    Returns:
        Filtered list of entities
    """
    whitelist_lower = {word.lower() for word in whitelist}
    return [
        entity for entity in entities
        if entity.text.lower() in whitelist_lower
    ]

def filter_by_fuzzy_match(
    entities: EntityList,
    pattern: str,
    threshold: float = 80.0
) -> EntityList:
    """Filter entities by fuzzy matching their text.

    Args:
        entities: List of EntityRecord instances
        pattern: Text pattern to match against
        threshold: Minimum similarity score (0-100)

    Returns:
        Filtered list of entities
    """
    return [
        entity for entity in entities
        if fuzz.partial_ratio(entity.text.lower(), pattern.lower()) >= threshold
    ]

def filter_by_regex(
    entities: EntityList,
    pattern: str
) -> EntityList:
    """Filter entities by regex pattern matching.

    Args:
        entities: List of EntityRecord instances
        pattern: Regex pattern to match against

    Returns:
        Filtered list of entities
    """
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        return [
            entity for entity in entities
            if regex.search(entity.text)
        ]
    except re.error:
        return entities  # Return all entities if regex is invalid

def filter_by_partial_word(
    entities: EntityList,
    word: str
) -> EntityList:
    """Filter entities that contain the given word as a substring.

    Args:
        entities: List of EntityRecord instances
        word: Word to search for

    Returns:
        Filtered list of entities
    """
    word_lower = word.lower()
    return [
        entity for entity in entities
        if word_lower in entity.text.lower()
    ]

def filter_by_length(
    entities: EntityList,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> EntityList:
    """Filter entities by their text length.

    Args:
        entities: List of EntityRecord instances
        min_length: Minimum text length
        max_length: Maximum text length

    Returns:
        Filtered list of entities
    """
    return [
        entity for entity in entities
        if (min_length is None or len(entity.text) >= min_length) and
           (max_length is None or len(entity.text) <= max_length)
    ]

def filter_all(
    entities: EntityList,
    config: FilterConfig
) -> EntityList:
    """Apply all configured filters to the entities.

    Args:
        entities: List of EntityRecord instances
        config: Filter configuration

    Returns:
        Filtered list of entities that match all configured filter criteria
    """
    filtered = entities

    if config.entity_types:
        filtered = filter_by_type(filtered, config.entity_types)

    if config.blacklist:
        filtered = filter_by_blacklist(filtered, config.blacklist)

    if config.whitelist:
        filtered = filter_by_whitelist(filtered, config.whitelist)

    if config.fuzzy_match:
        filtered = filter_by_fuzzy_match(
            filtered,
            config.fuzzy_match,
            config.fuzzy_threshold
        )

    if config.regex_pattern:
        filtered = filter_by_regex(filtered, config.regex_pattern)

    if config.partial_word:
        filtered = filter_by_partial_word(filtered, config.partial_word)

    if config.min_length is not None or config.max_length is not None:
        filtered = filter_by_length(
            filtered,
            config.min_length,
            config.max_length
        )

    return filtered
