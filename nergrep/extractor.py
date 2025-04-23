"""Entity extraction functionality."""

import spacy
from typing import List, Optional, Set
from .types import EntityRecord

# Load the English language model
nlp = spacy.load("en_core_web_lg")

def extract_entities(
    text: str,
    types: Optional[Set[str]] = None
) -> List[EntityRecord]:
    """Extract named entities from text.
    
    Args:
        text: Input text to process
        types: Optional set of entity types to include
        
    Returns:
        List of extracted entity records
    """
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        if types is None or ent.label_ in types:
            entities.append(EntityRecord(
                text=ent.text,
                label=ent.label_,
                sentence=ent.sent.text.strip(),
                start=ent.start_char,
                end=ent.end_char
            ))
    
    return entities 