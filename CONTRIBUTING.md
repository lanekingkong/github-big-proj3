# Contributing to BioOmicsBridge

Thank you for your interest in contributing to BioOmicsBridge—the world's first AI-native multi-omics data integration platform.

## Quick Links

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)

## How to Contribute

### 1. Reporting Bugs

Open an issue with:
- BioOmicsBridge version (`bioomics-bridge --version`)
- Python version (`python --version`)
- Operating system
- Minimal reproducible example
- Expected vs. actual behavior
- Error traceback (full)

### 2. Suggesting Features

Open an issue with:
- Problem statement (what pain point does this solve?)
- Proposed solution
- Alternatives considered
- Potential impact on existing features

### 3. Pull Request Process

```
1. Fork the repository
2. Create a feature branch: git checkout -b feature/amazing-feature
3. Write tests for your changes
4. Ensure all tests pass: pytest tests/
5. Format code: black . && isort .
6. Commit with clear message: git commit -m 'Add amazing feature'
7. Push to your fork: git push origin feature/amazing-feature
8. Open a Pull Request
```

### PR Guidelines

- **One feature per PR**: Keep changes focused
- **Tests required**: All new code must include tests
- **Documentation**: Update README and relevant docs
- **Type hints**: Use Python type hints throughout
- **Code style**: Follow PEP 8, enforced by black & isort
- **Commit messages**: Descriptive, present tense

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/BioOmicsBridge.git
cd BioOmicsBridge

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install development dependencies
pip install -e ".[dev,full]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v

# Format code
black bioomics_bridge/ tests/
isort bioomics_bridge/ tests/
```

## Project Structure

```
BioOmicsBridge/
├── bioomics_bridge/         # Core Python package
│   ├── ingest.py           # Data ingestion module
│   ├── harmonize.py        # Data harmonization module
│   ├── integrate.py        # Integration engine
│   ├── discover.py         # Target discovery engine
│   ├── agents/             # AI agent orchestration
│   ├── utils/              # Utility functions
│   └── cli.py              # Command-line interface
├── dashboard/              # Next.js web dashboard
├── docs/                   # Documentation
├── tests/                  # Test suite
├── examples/               # Example notebooks
├── setup.py                # Package setup
└── requirements.txt        # Dependencies
```

## Adding New Features

### Adding a New Omics Type

1. Add format detection in `bioomics_bridge/ingest.py`:
```python
OMICS_FORMATS["new_omics"] = {".ext1", ".ext2"}
```

2. Add normalization in `bioomics_bridge/harmonize.py`:
```python
def _normalize_newomics(self, data: Matrix) -> Matrix:
    # Implementation
    pass
```

3. Add agent in `bioomics_bridge/agents/__init__.py`:
```python
"newomics_preprocess": {
    "name": "NewOmics Preprocessing Agent",
    "description": "NewOmics data preprocessing",
    "capabilities": ["newomics_qc", "newomics_normalize"],
}
```

4. Add tests in `tests/test_new_omics.py`

### Adding a New Integration Method

1. Extend `MultiOmicsIntegrator` in `integrate.py`
2. Implement method with proper type hints
3. Add corresponding agent
4. Document in `API_REFERENCE.md`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=bioomics_bridge --cov-report=html

# Run specific test file
pytest tests/test_ingest.py -v

# Run with markers
pytest tests/ -v -m "integration"
```

## Release Process

1. Update version in `bioomics_bridge/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.x.x`
4. Push tag: `git push origin v1.x.x`
5. GitHub Actions will build and publish to PyPI

## Community

- **Questions**: GitHub Discussions
- **Bugs**: GitHub Issues
- **Feature requests**: GitHub Issues with label "enhancement"
- **Security vulnerabilities**: Email team@bioomicsbridge.org

## Recognition

Contributors will be listed in:
- `CONTRIBUTORS.md` file
- Release notes
- Project README acknowledgments