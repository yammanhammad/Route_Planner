# Contributing to Route Planner

Thank you for your interest in contributing to Route Planner! This document provides guidelines for contributing to the project.

**🚀 Just want to use the app?** Download the pre-built executable from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest) - no development setup required!

*Note: All Windows executables and cross-platform packages are automatically built and published using GitHub Actions CI/CD when releases are created.*

## Getting Started

### 🚀 Quick Setup (Recommended for Contributors)
```bash
# Clone and setup in one go
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
pip install -r requirements.txt
pip install -e .  # Install in development mode
python main.py    # Test the application
```

### 🔧 Full Development Setup (Advanced)
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Route_Planner.git
   cd Route_Planner
   ```
3. Set up the development environment:
   ```bash
   python scripts/setup_env.py
   pip install -e .
   ```
4. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### ✅ Verify Your Setup
```bash
# Test all entry points work
python main.py        # Direct execution
route-planner        # Installed command
./scripts/run_route_planner.sh  # Shell script (Linux/macOS)
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions focused and small

### Testing
- Write tests for new functionality
- Ensure all tests pass before submitting
- Maintain test coverage above 80%

### Documentation
- Update documentation for new features
- Include examples in docstrings
- Update README.md if necessary

## Submitting Changes

1. Ensure your code follows the style guidelines
2. Add or update tests as necessary
3. Update documentation
4. Submit a pull request with a clear description

## Reporting Issues

When reporting issues, please include:
- Operating system and version
- Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or logs

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment support

### Setup Steps
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
python scripts/setup_env.py
# Test the application manually
python main.py
```

## Code of Conduct

Please be respectful and professional in all interactions. We aim to create a welcoming environment for all contributors.

## License

By contributing to Route Planner, you agree that your contributions will be licensed under the MIT License.
