"""Tests for the entity extractor."""

from nergrep.extractor import extract_entities


def test_extract_entities_basic():
    text = "Apple Inc. is working with Microsoft on AI projects."
    entities = extract_entities(text)

    assert len(entities) > 0
    assert any(entity.text == "Apple Inc." for entity in entities)
    assert any(entity.text == "Microsoft" for entity in entities)

def test_extract_entities_with_types():
    text = "Apple Inc. is working with Microsoft on AI projects in New York."
    entities = extract_entities(text, types=["ORG"])

    assert len(entities) > 0
    assert all(entity.label == "ORG" for entity in entities)
    assert any(entity.text == "Microsoft" for entity in entities)
    assert not any(entity.text == "New York" for entity in entities)

def test_extract_entities_with_sentence_context():
    text = """Apple Inc. is a technology company.
    Microsoft is their competitor.
    Both companies are based in the United States."""

    entities = extract_entities(text)

    # Find Apple Inc. entity and check its sentence
    apple_entity = next(e for e in entities if e.text == "Apple Inc.")
    assert apple_entity.sentence == "Apple Inc. is a technology company."

    # Find Microsoft entity and check its sentence
    microsoft_entity = next(e for e in entities if e.text == "Microsoft")
    assert microsoft_entity.sentence == "Microsoft is their competitor."

def test_extract_entities_with_position():
    text = "Apple Inc. and Microsoft are tech companies."
    entities = extract_entities(text)

    apple_entity = next(e for e in entities if e.text == "Apple Inc.")
    assert apple_entity.start == 0
    assert apple_entity.end == 10  # "Apple Inc." is 10 characters long

    microsoft_entity = next(e for e in entities if e.text == "Microsoft")
    assert microsoft_entity.start == 15  # Account for "and " after "Apple Inc."
    assert microsoft_entity.end == 24  # 15 + len("Microsoft")
