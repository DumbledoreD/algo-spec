#!/bin/bash

# Install python requirements
python -m pip install --upgrade pip
python -m pip install --user -r ./requirements.txt

# Set up pre-commit
pre-commit install
pre-commit autoupdate
