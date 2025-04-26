"""Tests for the entity filters."""

import pytest

from nergrep.filters import (
    FilterConfig,
    filter_all,
    filter_by_blacklist,
    filter_by_fuzzy_match,
    filter_by_length,
    filter_by_partial_word,
    filter_by_regex,
    filter_by_type,
    filter_by_whitelist,
)
from nergrep.types import EntityRecord


@pytest.fixture
def sample_entities():
    return [
        EntityRecord(
            text="Apple Inc.",
            label="ORG",
            sentence="Apple Inc. is a company.",
            start=0,
            end=9
        ),
        EntityRecord(
            text="Microsoft",
            label="ORG",
            sentence="Microsoft develops software.",
            start=0,
            end=9
        ),
        EntityRecord(
            text="John Smith",
            label="PERSON",
            sentence="John Smith is a developer.",
            start=0,
            end=10
        ),
        EntityRecord(
            text="New York",
            label="GPE",
            sentence="They are based in New York.",
            start=18,
            end=26
        ),
        EntityRecord(
            text="Google",
            label="ORG",
            sentence="Google is a search engine.",
            start=0,
            end=6
        ),
        EntityRecord(
            text="Jane Doe",
            label="PERSON",
            sentence="Jane Doe works there.",
            start=0,
            end=8
        ),
        EntityRecord(
            text="London",
            label="GPE",
            sentence="The office is in London.",
            start=17,
            end=23
        )
    ]

def test_filter_by_type(sample_entities):
    filtered = filter_by_type(sample_entities, {"ORG"})
    assert len(filtered) == 3
    assert all(entity.label == "ORG" for entity in filtered)

def test_filter_by_blacklist(sample_entities):
    blacklist = {"Microsoft", "New York"}
    filtered = filter_by_blacklist(sample_entities, blacklist)
    assert len(filtered) == 5
    assert not any(entity.text in blacklist for entity in filtered)

def test_filter_by_blacklist_case_insensitive(sample_entities):
    blacklist = {"microsoft", "NEW YORK"}
    filtered = filter_by_blacklist(sample_entities, blacklist)
    assert len(filtered) == 5
    assert not any(entity.text.lower() in {word.lower() for word in blacklist} for entity in filtered)

def test_filter_by_whitelist(sample_entities):
    whitelist = {"Apple Inc.", "Google", "London"}
    filtered = filter_by_whitelist(sample_entities, whitelist)
    assert len(filtered) == 3
    assert all(entity.text in whitelist for entity in filtered)

def test_filter_by_whitelist_case_insensitive(sample_entities):
    whitelist = {"apple inc.", "GOOGLE", "London"}
    filtered = filter_by_whitelist(sample_entities, whitelist)
    assert len(filtered) == 3
    assert all(entity.text.lower() in {word.lower() for word in whitelist} for entity in filtered)

def test_filter_by_fuzzy_match(sample_entities):
    filtered = filter_by_fuzzy_match(sample_entities, "micro")
    assert len(filtered) == 1
    assert filtered[0].text == "Microsoft"

def test_filter_by_regex(sample_entities):
    # Test basic regex matching
    filtered = filter_by_regex(sample_entities, r"^[A-Z]")
    assert len(filtered) == 7  # All entities start with capital letter

    # Test case-insensitive matching
    filtered = filter_by_regex(sample_entities, r"apple")
    assert len(filtered) == 1
    assert filtered[0].text == "Apple Inc."

    # Test invalid regex
    filtered = filter_by_regex(sample_entities, r"[")
    assert len(filtered) == 7  # Should return all entities for invalid regex

def test_filter_by_partial_word(sample_entities):
    # Test basic partial word matching
    filtered = filter_by_partial_word(sample_entities, "soft")
    assert len(filtered) == 1
    assert filtered[0].text == "Microsoft"

    # Test case-insensitive matching
    filtered = filter_by_partial_word(sample_entities, "APPLE")
    assert len(filtered) == 1
    assert filtered[0].text == "Apple Inc."

def test_filter_by_length(sample_entities):
    # Test minimum length
    filtered = filter_by_length(sample_entities, min_length=6)
    assert len(filtered) == 7  # All entities are at least 6 characters long
    assert all(len(entity.text) >= 6 for entity in filtered)

    # Test maximum length
    filtered = filter_by_length(sample_entities, max_length=6)
    assert len(filtered) == 2  # Only "Google" and "London" are 6 characters or less
    assert all(len(entity.text) <= 6 for entity in filtered)
    assert {entity.text for entity in filtered} == {"Google", "London"}

    # Test both min and max length
    filtered = filter_by_length(sample_entities, min_length=6, max_length=8)
    assert len(filtered) == 4  # "New York", "Google", "Jane Doe", "London" are between 6 and 8 characters
    assert all(6 <= len(entity.text) <= 8 for entity in filtered)
    assert {entity.text for entity in filtered} == {"New York", "Google", "Jane Doe", "London"}

def test_filter_all_with_multiple_filters(sample_entities):
    config = FilterConfig(
        entity_types={"ORG"},  # Only ORG entities
        blacklist={"Microsoft"},  # Exclude Microsoft
        whitelist={"Google"},  # Only include Google
        fuzzy_match="goo",  # Must match "goo"
        regex_pattern=r"^[A-Z]",  # Must start with capital letter
        min_length=5,  # Must be at least 5 characters
        max_length=6  # Must be at most 6 characters
    )
    filtered = filter_all(sample_entities, config)
    assert len(filtered) == 1
    assert filtered[0].text == "Google"

def test_filter_all_with_blacklist_and_whitelist(sample_entities):
    config = FilterConfig(
        blacklist={"Microsoft", "Google"},
        whitelist={"Apple Inc.", "Google", "Microsoft"}
    )
    filtered = filter_all(sample_entities, config)
    assert len(filtered) == 1
    assert filtered[0].text == "Apple Inc."
