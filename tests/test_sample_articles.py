"""Tests for entity extraction from sample articles."""

from pathlib import Path

import pytest

from nergrep.extractor import extract_entities
from nergrep.filters import FilterConfig, filter_all


@pytest.fixture
def sample_text():
    return Path("test_data/sample_articles.txt").read_text()

def test_extract_organizations(sample_text):
    """Test extraction of organization entities."""
    entities = extract_entities(sample_text)
    orgs = filter_all(entities, FilterConfig(entity_types={"ORG"}))
    expected_orgs = {
        "The Allman Brothers Band",
        "The Marshall Tucker Band",
        "Google",
        "Instagram",
        "Spotify",
        "The Python Software Foundation",
        "Warner Bros. Leone's",
        "Royal Mail",
        "Bayer",
        "The U.S. Food and Drug Administration",
        "The World Health Organization",
        "Microsoft Corporation",
        "NASA",
        "ESA",
        "the Canadian Space Agency",
        "SpaceX",
        "CWI",
        "The International Space Station",
        "Abbey Road Studios",
        "BC",
        "Python"
    }
    found_orgs = {entity.text for entity in orgs}
    print("\nFound organizations:", found_orgs)
    print("Missing organizations:", expected_orgs - found_orgs)
    assert expected_orgs.issubset(found_orgs)

def test_extract_persons(sample_text):
    """Test extraction of person entities."""
    entities = extract_entities(sample_text)
    persons = filter_all(entities, FilterConfig(entity_types={"PERSON"}))
    expected_persons = {
        "Guido van Rossum",
        "Alexander the Great",
        "Sergio Leone",
        "Clint Eastwood",
        "Robert De Niro",
        "Quentin Tarantino",
        "Henry VIII",
        "Rowland Hill's",
        "Felix Hoffmann",
        "Bill Gates",
        "Paul Allen",
        "Elon Musk",
        "John Lennon",
        "Paul McCartney",
        "George Harrison",
        "Ringo Starr",
        "George Martin",
        "Edmund Hillary",
        "Tenzing Norgay",
        "Sherpa",
        "Beatles",
        "Lynyrd Skynyrd"
    }
    found_persons = {entity.text for entity in persons}
    print("\nFound persons:", found_persons)
    print("Missing persons:", expected_persons - found_persons)
    assert expected_persons.issubset(found_persons)

def test_extract_locations(sample_text):
    """Test extraction of location entities."""
    entities = extract_entities(sample_text)
    locations = filter_all(entities, FilterConfig(entity_types={"GPE", "LOC"}))
    expected_locations = {
        "Jacksonville",
        "Florida",
        "South Carolina",
        "Netherlands",
        "the Hellenic Republic",
        "Europe",
        "Athens",
        "Albuquerque",
        "New Mexico",
        "Redmond",
        "Washington",
        "Liverpool",
        "Mount Everest",
        "Tibet Autonomous Region",
        "the British Empire",
        "Southern Rock",
        "The Penny Black"
    }
    found_locations = {entity.text for entity in locations}
    print("\nFound locations:", found_locations)
    print("Missing locations:", expected_locations - found_locations)
    assert expected_locations.issubset(found_locations)

def test_date_extraction(sample_text):
    """Test extraction of date entities."""
    entities = extract_entities(sample_text)
    dates = filter_all(entities, FilterConfig(entity_types={"DATE"}))
    expected_dates = {
        "the 1970s",
        "1991",
        "2001",
        "the 5th century",
        "1984",
        "1840",
        "1897",
        "1899",
        "1975",
        "1985",
        "2000",
        "1960",
        "1953"
    }
    found_dates = {entity.text for entity in dates}
    print("\nFound dates:", found_dates)
    print("Missing dates:", expected_dates - found_dates)
    assert expected_dates.issubset(found_dates)
