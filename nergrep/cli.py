"""Command-line interface for nergrep."""

import typer
from pathlib import Path
from typing import List, Optional
import json
from .extractor import extract_entities
from .filters import FilterConfig, filter_all
from .types import EntityRecord

app = typer.Typer()

def format_entity(entity: EntityRecord, format_type: str = "text") -> str:
    """Format an entity record for output.
    
    Args:
        entity: The entity record to format
        format_type: Output format type ("text", "json", or "csv")
        
    Returns:
        Formatted string representation of the entity
    """
    if format_type == "json":
        return json.dumps({
            "text": entity.text,
            "label": entity.label,
            "sentence": entity.sentence,
            "start": entity.start,
            "end": entity.end
        })
    elif format_type == "csv":
        return f'"{entity.text}","{entity.label}","{entity.sentence}",{entity.start},{entity.end}'
    else:  # text format
        return f"{entity.text} ({entity.label}) in: {entity.sentence}"

@app.command()
def main(
    input_file: str = typer.Argument(..., help="Input text file to process"),
    types: Optional[str] = typer.Option(
        None,
        "--types",
        "-t",
        help="Entity types to include, comma-separated (e.g., PERSON,ORG,GPE)"
    ),
    fuzzy: Optional[str] = typer.Option(
        None,
        "--fuzzy",
        "-f",
        help="Fuzzy match pattern to filter entities"
    ),
    blacklist_file: Optional[str] = typer.Option(
        None,
        "--blacklist",
        "-b",
        help="File containing blacklisted terms"
    ),
    whitelist_file: Optional[str] = typer.Option(
        None,
        "--whitelist",
        "-w",
        help="File containing whitelisted terms"
    ),
    fuzzy_threshold: float = typer.Option(
        80.0,
        "--threshold",
        help="Minimum similarity score for fuzzy matching (0-100)"
    ),
    regex: Optional[str] = typer.Option(
        None,
        "--regex",
        "-r",
        help="Regex pattern to match against entity text"
    ),
    partial_word: Optional[str] = typer.Option(
        None,
        "--partial",
        "-p",
        help="Word that must be contained in entity text"
    ),
    min_length: Optional[int] = typer.Option(
        None,
        "--min-length",
        help="Minimum length of entity text"
    ),
    max_length: Optional[int] = typer.Option(
        None,
        "--max-length",
        help="Maximum length of entity text"
    ),
    output_format: str = typer.Option(
        "text",
        "--format",
        "-o",
        help="Output format: text, json, or csv"
    ),
    include_sentence: bool = typer.Option(
        True,
        "--include-sentence/--no-sentence",
        help="Include the full sentence context in output"
    ),
    sort_by: Optional[str] = typer.Option(
        None,
        "--sort",
        "-s",
        help="Sort output by: text, label, position, length, or frequency"
    )
):
    """Extract named entities from text with optional filtering."""
    
    # Convert paths to Path objects
    input_path = Path(input_file)
    blacklist_path = Path(blacklist_file) if blacklist_file else None
    whitelist_path = Path(whitelist_file) if whitelist_file else None
    
    # Read input text
    text = input_path.read_text()
    
    # Read blacklist if provided
    blacklist = None
    if blacklist_path:
        blacklist = set(blacklist_path.read_text().splitlines())
    
    # Read whitelist if provided
    whitelist = None
    if whitelist_path:
        whitelist = set(whitelist_path.read_text().splitlines())
    
    # Extract entities
    entity_types = set(types.split(",")) if types else None
    entities = extract_entities(text, types=entity_types)
    
    # Apply filters
    if any([blacklist, whitelist, fuzzy, regex, partial_word, min_length, max_length]):
        filter_config = FilterConfig(
            entity_types=entity_types,
            blacklist=blacklist,
            whitelist=whitelist,
            fuzzy_match=fuzzy,
            fuzzy_threshold=fuzzy_threshold,
            regex_pattern=regex,
            partial_word=partial_word,
            min_length=min_length,
            max_length=max_length
        )
        entities = filter_all(entities, filter_config)
    
    # Sort entities if requested
    if sort_by:
        if sort_by == "text":
            entities.sort(key=lambda x: x.text.lower())
        elif sort_by == "label":
            entities.sort(key=lambda x: (x.label, x.text.lower()))
        elif sort_by == "position":
            entities.sort(key=lambda x: x.start)
        elif sort_by == "length":
            entities.sort(key=lambda x: len(x.text))
        elif sort_by == "frequency":
            # Count entity occurrences
            entity_counts = {}
            for entity in entities:
                key = (entity.text, entity.label)
                entity_counts[key] = entity_counts.get(key, 0) + 1
            # Sort by frequency (descending) and then by text
            entities.sort(key=lambda x: (-entity_counts[(x.text, x.label)], x.text.lower()))
    
    # Output results
    if output_format == "json":
        print(json.dumps([{
            "text": e.text,
            "label": e.label,
            "sentence": e.sentence if include_sentence else "",
            "start": e.start,
            "end": e.end
        } for e in entities], indent=2))
    elif output_format == "csv":
        if include_sentence:
            print("text,label,sentence,start,end")
            for entity in entities:
                print(format_entity(entity, "csv"))
        else:
            print("text,label,start,end")
            for entity in entities:
                print(f'"{entity.text}","{entity.label}",{entity.start},{entity.end}')
    else:  # text format
        for entity in entities:
            if include_sentence:
                print(format_entity(entity, "text"))
            else:
                print(f"{entity.text} ({entity.label})")

if __name__ == "__main__":
    app() 