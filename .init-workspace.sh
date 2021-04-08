#!/bin/bash

# Set up pre-commit
python3 -m pip install --user pre-commit
pre-commit install
pre-commit autoupdate

# Pytest
python3 -m pip install --user pytest
