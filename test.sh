#!/bin/bash

# Activate virtual environment and run Python tests
source venv/bin/activate
python3 test.py

# Run Postman collections with Newman
newman run forum_multiple_posts.postman_collection.json -e env.json
newman run forum_post_read_delete.postman_collection.json -e env.json