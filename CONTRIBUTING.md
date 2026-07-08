# Contributing to RAG PDF Chatbot

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

### Prerequisites
- Python 3.9+
- Git
- OpenAI API key

### Local Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/RAG-PDF-CHATBOT.git
   cd RAG-PDF-CHATBOT
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
# or
git checkout -b docs/documentation-update
```

### Code Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use type hints for function parameters and return types
- Write docstrings for all functions and classes
- Keep functions focused and single-responsibility

### Example Code Style

```python
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def process_pdf(file_path: str, extract_tables: bool = True) -> dict:
    """
    Process PDF file and extract text.
    
    Args:
        file_path: Path to PDF file
        extract_tables: Whether to extract table data
    
    Returns:
        Dictionary containing extracted text and metadata
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If PDF is corrupted
    """
    try:
        logger.info(f"Processing PDF: {file_path}")
        # Implementation here
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to process PDF: {str(e)}")
        raise
```

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Submitting Changes

### Commit Messages

```
feat: Add new feature description
fix: Fix bug description
docs: Update documentation
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

### Pull Request Process

1. Push your branch to your fork
2. Create a Pull Request against `main` branch
3. Fill in the PR template completely
4. Ensure all CI/CD checks pass
5. Request review from maintainers
6. Address feedback and update PR
7. Once approved, PR will be merged

## Reporting Bugs

Use the GitHub Issues template:
- **Title**: Clear, descriptive title
- **Environment**: Python version, OS, key dependencies
- **Steps to Reproduce**: Clear steps to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable

## Suggesting Enhancements

- Use the feature request template
- Explain the use case
- Describe the expected behavior
- Provide examples if possible

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report inappropriate behavior to maintainers

## Questions?

Feel free to:
- Open an issue for discussion
- Check existing issues/discussions
- Contact: dev.vivekrana@gmail.com

Thank you for contributing! 🚀
