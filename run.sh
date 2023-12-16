#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Start the Flask server
export FLASK_APP=app.py
export FLASK_ENV=development
exec flask run
