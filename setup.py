import pathlib

from setuptools import find_packages, setup

# Read the contents of README.md
here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="nergrep",
    version="0.1.0",
    description=(
        "A flexible Python package for extracting and filtering named entities "
        "with semantic text compression"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",  # TODO: Update with your name
    author_email="your.email@example.com",  # TODO: Update with your email
    url=(
        "https://github.com/yourusername/nergrep"  # TODO: Update with your repository URL
    ),
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0.0",
        "typer>=0.9.0",
        "rapidfuzz>=3.0.0",
        "langchain>=0.1.0",
        "openai>=1.0.0",
        "langchain-openai>=0.0.5",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "ruff>=0.3.0",
        ],
        "langchain": [
            "langchain>=0.1.0",
            "langchain-community>=0.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "nergrep=nergrep.cli:app",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords=(
        "nlp, named-entity-recognition, spacy, text-processing, "
        "semantic-compression"
    ),
)
