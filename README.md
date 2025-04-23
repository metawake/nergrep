# Nergrep

A flexible Python package for extracting and filtering named entities from text using spaCy, with semantic text compression capabilities.

## Features

- Extract named entities using spaCy
- Semantic text compression with configurable profiles:
  - `safe` mode: preserves core information, removes trivial filler
  - `quality` mode: aggressively removes modifiers and redundant phrases
- Filter entities by:
  - Entity type (PERSON, ORG, GPE, etc.)
  - Fuzzy text matching
  - Blacklist exclusion
  - Whitelist inclusion
  - Combined filtering with AND logic
- Use as a CLI tool or Python module
- Multiple output formats (text, JSON, CSV)
- Sentence context for each entity
- Sorting options
- Case-insensitive matching

## Installation

1. Install from PyPI:
```bash
pip install nergrep
```

2. Download the spaCy model:
```bash
python -m spacy download en_core_web_lg
```

## Usage

### As a Python Module

```python
from nergrep.extractor import extract_entities
from nergrep.filters import FilterConfig, filter_all
from nergrep.types import EntityRecord

# Basic extraction
text = "Apple Inc. is working with Microsoft on AI projects."
entities = extract_entities(text)

# Extract with type filtering
entities = extract_entities(text, types=["ORG"])

# Extract with filters
filter_config = FilterConfig(
    entity_types={"ORG"},
    blacklist={"Google"},
    whitelist={"Apple Inc.", "Microsoft"},
    fuzzy_match="micro",
    fuzzy_threshold=80.0
)
filtered_entities = filter_all(entities, filter_config)

# Access entity information
for entity in entities:
    print(f"Text: {entity.text}")
    print(f"Label: {entity.label}")
    print(f"Sentence: {entity.sentence}")
    print(f"Position: {entity.start}-{entity.end}")
```

### Semantic Text Compression

```python
from nergrep.compression import compress_text

# Safe mode - preserves core information
compressed = compress_text(text, profile="safe")

# Quality mode - more aggressive compression
compressed = compress_text(text, profile="quality")

# Custom compression with specific rules
compressed = compress_text(text, 
    remove_fillers=True,
    remove_greetings=True,
    strip_modifiers=False,
    collapse_phrases=True
)
```

### As a CLI Tool

```bash
# Basic usage
nergrep extract input.txt

# With filters
nergrep extract input.txt \
    --types ORG PERSON \
    --fuzzy "coin" \
    --blacklist blacklist.txt \
    --whitelist whitelist.txt \
    --threshold 85.0 \
    --format json \
    --include-sentence \
    --sort text

# Output formats
nergrep extract input.txt --format text    # Human-readable text
nergrep extract input.txt --format json    # JSON output
nergrep extract input.txt --format csv     # CSV output

# Sorting options
nergrep extract input.txt --sort text      # Sort by entity text
nergrep extract input.txt --sort label     # Sort by entity type
nergrep extract input.txt --sort position  # Sort by position in text
nergrep extract input.txt --sort frequency # Sort by occurrence frequency
```

## CLI Options

- `input`: Input text file to process
- `--types` / `-t`: Entity types to include (e.g., PERSON, ORG, GPE)
- `--fuzzy` / `-f`: Fuzzy match pattern to filter entities
- `--blacklist` / `-b`: File containing blacklisted terms
- `--whitelist` / `-w`: File containing whitelisted terms
- `--threshold`: Minimum similarity score for fuzzy matching (0-100)
- `--format` / `-o`: Output format (text, json, or csv)
- `--include-sentence/--no-sentence`: Include/exclude sentence context
- `--sort` / `-s`: Sort output by text, label, position, or frequency

## Development

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT 