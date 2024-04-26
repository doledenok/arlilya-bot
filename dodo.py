#!usr/bin/env python3
"""Project tasks."""

import glob


DOIT_CONFIG = {'default_tasks': ['wheel']}

def task_html():
    """Build documentation-html for project."""
    return {
        'actions': ['make -C docs html'],
        'file_dep' : glob.glob("*.py") + glob.glob("*.rst"),
    }

def task_gitclean():
    """Clean untracked files."""
    return {
            'actions': ['git clean -xdf'],
    }

def task_test():
    """Test application."""
    yield {
            'actions': ['pytest test/tests_exam.py', 'pytest test/tests_statistics.py'], 'name': "any_tests",
            'verbosity': 2
    }


def task_docstyle():
    """Check docstrings in src code files."""
    return {
            'actions': ['pydocstyle ./src'],
            'verbosity': 2
    }

def task_analyze():
    """Check code in src directory."""
    return {
            'actions': ['flake8 ./src'],
            'verbosity': 2
    }

def task_check():
    """Perform all checks."""
    return {
            'actions': [],
            'task_dep': ['analyze', 'docstyle', 'test']
    }

def task_wheel():
    """Build wheel."""
    return {
            'actions': ['python3 -m build -w'],
            'task_dep': ['gitclean'],
    }

def task_start():
    """Run bot."""
    return {
        'actions': ['python3 src/main.py'],
        'verbosity': 2,
    }
