# Development Guide

This guide provides detailed information for developers working on or contributing to the Route Planner project.

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- Git
- (Windows only) Visual Studio Build Tools with C++ support

### Setting Up Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yammanhammad/Route_Planner.git
   cd Route_Planner
   ```

2. **Set up environment**
   ```bash
   python scripts/setup_env.py
   ```
   This script will:
   - Create a virtual environment
   - Install dependencies from requirements.txt
   - Set up pre-commit hooks
   - Configure development settings

3. **Verify setup**
   ```bash
   python main.py --dev
   ```
   The application should start in development mode.

## Project Structure

```
Route_Planner/
├── main.py                    # Application launcher
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── route_planner.py           # Cross-platform launcher
├── route_planner/             # Main application package
│   ├── __init__.py            # Package initialization
│   ├── app.py                 # Core application with UI
│   ├── algorithms/            # Routing algorithms
│   ├── ui/                    # User interface components
│   └── utils/                 # Utility functions
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
└── cache/                     # Runtime cache
```

See subdirectory READMEs for more detailed information about specific components.

## Development Workflow

### Branching Strategy
- `main` - stable production code
- `develop` - integration branch for features
- `feature/xxx` - feature branches
- `fix/xxx` - bug fix branches
- `release/x.x.x` - release preparation

### Commit Guidelines
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Reference issues in commit message body
- Include details about why a change is needed

### Pull Request Process
1. Create a branch from `develop`
2. Implement your changes
3. Update documentation if necessary
4. Submit a pull request to `develop`
5. Wait for code review
6. Make requested changes
7. Merge after approval

## Testing

Since this project currently doesn't have formal unit tests, ensure manual testing covers:
- Application startup and GUI loading
- Route optimization functionality  
- Map display and interaction
- Configuration loading
- Cross-platform compatibility

## Building and Packaging

### Windows Executables
Windows executables are built automatically by GitHub Actions CI/CD:

1. A workflow is triggered when:
   - A new release is created
   - A tag with pattern 'v*' is pushed
   - Manually triggered from GitHub

2. The workflow uses:
   - `scripts/windows_build.spec` - PyInstaller configuration
   - `scripts/runtime_hook_vcruntime.py` - Runtime hooks
   - `scripts/installer.nsi` - NSIS installer script

### Cross-Platform Packages
For other platforms, use the scripts directory tools:

```bash
# Set up development environment
python scripts/setup_env.py

# Install package for distribution
python scripts/install.py
```

## Documentation

### Documentation Structure
- `README.md` - Project overview and quick start
- `DEVELOPMENT.md` - This developer guide
- `docs/` - Detailed documentation
  - `RELEASE_NOTES.md` - Version history
  - `WINDOWS_GUIDE.md` - Windows-specific guide
  - `CONTRIBUTING.md` - Contribution guidelines

### Documentation Guidelines
- Use Markdown for all documentation
- Include code examples where appropriate
- Keep documentation up-to-date with code changes
- Use headings and lists for readability
- Include images or diagrams when helpful

## Continuous Integration

The project uses GitHub Actions for CI/CD:

- **test.yml** - Runs on every pull request and push to main/develop
  - Runs tests on multiple Python versions
  - Generates code coverage report
  - Validates code style

- **build.yml** - Runs on release creation
  - Builds Windows executables
  - Creates distribution packages
  - Uploads assets to GitHub Releases

## Release Process

1. Update version number in:
   - `config.py`
   - `route_planner/__init__.py`
   - `setup.py`

2. Update `docs/RELEASE_NOTES.md` with changes

3. Create a release branch:
   ```bash
   git checkout -b release/x.x.x
   ```

4. Create pull request to `main`

5. After merge, tag the release:
   ```bash
   git tag -a vx.x.x -m "Version x.x.x"
   git push origin vx.x.x
   ```

6. Create a GitHub Release with release notes

## Architecture

### Core Components
- **UI Layer** - PyQt5-based interface with WebEngine
- **Algorithm Layer** - Route optimization algorithms
- **Data Layer** - Caching and persistence
- **API Layer** - External service integration

### Key Design Patterns
- **Model-View-Controller** - For UI separation
- **Worker Threads** - For background processing
- **Factory Pattern** - For algorithm selection
- **Singleton** - For configuration and logging

## Support and Community

- **Issue Tracker**: [GitHub Issues](https://github.com/yammanhammad/Route_Planner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yammanhammad/Route_Planner/discussions)
- **Contributing**: See [CONTRIBUTING.md](docs/CONTRIBUTING.md)
