#!/bin/bash

# Set up pre-commit
python3.8 -m pip install --user pre-commit
pre-commit install
pre-commit autoupdate