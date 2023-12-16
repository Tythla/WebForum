#!/bin/bash
python3 app.py &
APP_PID=$!
python3 test.py

# Run Postman collections with Newman
newman run forum_multiple_posts.postman_collection.json -e env.json
newman run forum_post_read_delete.postman_collection.json -e env.json

kill APP_PID=$!