"""
Pytest configuration and fixtures.

This file is automatically loaded by pytest and provides:
- Custom command-line options
- Shared fixtures
- Test configuration
"""

import pytest


def pytest_addoption(parser):
    """Add custom command-line options to pytest."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests (requires OpenAI API key and network access)"
    )


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers",
        "integration: Integration tests that may require external services (use --run-integration to run)"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip integration tests by default."""
    if config.getoption("--run-integration"):
        # If --run-integration is specified, run all tests
        return
    
    # Otherwise, skip integration tests
    skip_integration = pytest.mark.skip(reason="Integration tests skipped (use --run-integration to run)")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)

