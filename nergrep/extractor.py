"""Entity extraction functionality."""

from typing import List, Optional, Set

import spacy
from spacy.matcher import PhraseMatcher

from .types import EntityRecord

# Initialize spaCy model and custom entity patterns
try:
    # Load the English language model
    nlp = spacy.load("en_core_web_lg")
except OSError as err:
    raise RuntimeError(
        "spaCy model 'en_core_web_lg' not found. "
        "Please install it using: python -m spacy download en_core_web_lg"
    ) from err

# Add custom entity patterns
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
org_patterns = [
    "Python Software Foundation",
    "The Python Software Foundation",
    "CWI",
    "PSF"
]
patterns = [nlp(text) for text in org_patterns]
matcher.add("ORG", patterns)

def extract_entities(
    text: str,
    types: Optional[Set[str]] = None
) -> List[EntityRecord]:
    """Extract named entities from text using spaCy's NER model.

    Args:
        text: Input text to process
        types: Optional set of entity types to include (e.g., {'PERSON', 'ORG', 'GPE'})

    Returns:
        List of extracted entity records containing text, label, sentence context,
        and character positions

    Raises:
        RuntimeError: If spaCy model is not properly loaded
    """
    doc = nlp(text)
    entities = []

    # Add custom matches first
    matches = matcher(doc)
    for _match_id, start, end in matches:
        span = doc[start:end]
        if types is None or "ORG" in types:
            entities.append(EntityRecord(
                text=span.text,
                label="ORG",
                sentence=span.sent.text.strip(),
                start=span.start_char,
                end=span.end_char
            ))

    # Then add spaCy's NER matches
    for ent in doc.ents:
        # Skip if we already have a custom match for this span
        if any(e.start == ent.start_char and e.end == ent.end_char for e in entities):
            continue
        if types is None or ent.label_ in types:
            entities.append(EntityRecord(
                text=ent.text,
                label=ent.label_,
                sentence=ent.sent.text.strip(),
                start=ent.start_char,
                end=ent.end_char
            ))

    return entities
