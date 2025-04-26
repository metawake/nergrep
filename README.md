# Nergrep

+ As an AI/NLP/ML platform engineer, I often need to prototype and iterate on text analytics pipelines. Entity extraction is a frequent, foundational step—whether I'm building quick R&D experiments or shaping components for production. I wanted a tool that was both fast and flexible: something I could use from the command line for ad-hoc analysis, or drop into Python code and larger frameworks like Langchain for more complex workflows.
+ 
+ That's why I built `nergrep`: a Python package and CLI for extracting and filtering named entities using spaCy, with powerful filtering and seamless integration into modern LLM pipelines.
+ 
+ While I'm still exploring whether `nergrep` will become a production staple or remain a rapid prototyping tool, it's already proven invaluable for shaping and testing new NLP pipelines in R&D.

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

# Quick Demo

```bash
nergrep "Apollo 11 was the spaceflight that first landed humans on the Moon. Commander Neil Armstrong and lunar module pilot Buzz Aldrin formed the American crew. They landed the Apollo Lunar Module Eagle on July 20, 1969, at 20:17 UTC. They collected 47.5 pounds of lunar material to bring back to Earth. The mission was launched by a Saturn V rocket from Kennedy Space Center in Florida, and fulfilled a national goal set by President John F. Kennedy in 1961. NASA was responsible for the mission."
```

# Example output: YAML output from nergrep entity extraction
```
- text: "Apollo"
  label: "ORG"
  sentence: "Apollo 11 was the spaceflight that first landed humans on the Moon."
- text: "Neil Armstrong"
  label: "PERSON"
  sentence: "Commander Neil Armstrong and lunar module pilot Buzz Aldrin formed the American crew."
- text: "July 20, 1969"
  label: "DATE"
  sentence: "They landed the Apollo Lunar Module Eagle on July 20, 1969, at 20:17 UTC."
- text: "Earth"
  label: "LOC"
  sentence: "They collected 47.5 pounds of lunar material to bring back to Earth."
- text: "NASA"
  label: "ORG"
  sentence: "The mission was launched by a Saturn V rocket from Kennedy Space Center in Florida, and fulfilled a national goal set by President John F. Kennedy in 1961."
```

## Installation

```bash
pip install git+https://github.com/metawake/nergrep.git
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
