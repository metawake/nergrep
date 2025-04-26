# Nergrep

A flexible Python package for extracting and filtering named entities from text using spaCy.

## Features

- Extract named entities using spaCy
- Filter entities by:
  - Entity type (PERSON, ORG, GPE, etc.)
  - Fuzzy text matching
  - Blacklist exclusion
  - Whitelist inclusion
  - Regex pattern matching
  - Partial word matching
  - Length constraints
  - Combined filtering with AND logic
- Use as a CLI tool or Python module
- Multiple output formats (text, JSON, CSV)
- Sentence context for each entity
- Sorting options
- Case-insensitive matching

## Installation

```bash
pip install git+https://github.com/yourusername/nergrep.git
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
    fuzzy_threshold=80.0,
    regex_pattern="^[A-Z]",
    partial_word="soft",
    min_length=5,
    max_length=20
)
filtered_entities = filter_all(entities, filter_config)

# Access entity information
for entity in entities:
    print(f"Text: {entity.text}")
    print(f"Label: {entity.label}")
    print(f"Sentence: {entity.sentence}")
    print(f"Position: {entity.start}-{entity.end}")
```

### As a CLI Tool

```bash
# Basic usage with text input
nergrep "The Python Software Foundation was established in 2001"

# Basic usage with file input
nergrep input.txt

# With filters
nergrep "Microsoft Corporation was founded by Bill Gates" \
    --types ORG,PERSON \
    --fuzzy "micro" \
    --threshold 80.0 \
    --regex "^[A-Z]" \
    --partial "soft" \
    --min-length 5 \
    --max-length 20 \
    --format json \
    --include-sentence \
    --sort text

# Output formats
nergrep "text" --format text    # Human-readable text
nergrep "text" --format json    # JSON output
nergrep "text" --format csv     # CSV output

# Sorting options
nergrep "text" --sort text      # Sort by entity text
nergrep "text" --sort label     # Sort by entity type
nergrep "text" --sort position  # Sort by position in text
nergrep "text" --sort length    # Sort by entity length
nergrep "text" --sort frequency # Sort by occurrence frequency
```

## CLI Options

- `input_text`: Input text or file path to process
- `--types` / `-t`: Entity types to include (e.g., PERSON,ORG,GPE)
- `--fuzzy` / `-f`: Fuzzy match pattern to filter entities
- `--blacklist` / `-b`: File containing blacklisted terms
- `--whitelist` / `-w`: File containing whitelisted terms
- `--threshold`: Minimum similarity score for fuzzy matching (0-100)
- `--regex` / `-r`: Regex pattern to match against entity text
- `--partial` / `-p`: Word that must be contained in entity text
- `--min-length`: Minimum length of entity text
- `--max-length`: Maximum length of entity text
- `--format` / `-o`: Output format (text, json, or csv)
- `--include-sentence/--no-sentence`: Include/exclude sentence context
- `--sort` / `-s`: Sort output by text, label, position, length, or frequency

## Development

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest tests/
```

5. Run linting:
```bash
ruff check .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT