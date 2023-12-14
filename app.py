from flask import Flask, request, jsonify, abort
import datetime
import os
import threading

app = Flask(__name__)


@app.get("/random/<int:sides>")
def roll(sides):
    if sides <= 0:
        return {'err': 'need a positive number of sides'}, 400

    return {'num': randbelow(sides) + 1 }

posts = {}
post_id = 0
lock = threading.Lock()

@app.route('/post', methods=['POST'])
def create_post():
    global post_id
    content = request.json

    if not content or 'msg' not in content or not isinstance(content['msg'], str):
        return jsonify(error="Bad Request"), 400

    with lock:
        post_id += 1
        key = os.urandom(24).hex()
        timestamp = datetime.datetime.utcnow().isoformat()
        posts[post_id] = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': content['msg']}

    return jsonify(id=post_id, key=key, timestamp=timestamp)

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    with lock:
        if post_id in posts:
            post = posts[post_id]
            return jsonify(id=post['id'], timestamp=post['timestamp'], msg=post['msg'])
        else:
            abort(404, description="Post not found")

@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    with lock:
        if post_id in posts:
            post = posts[post_id]
            if post['key'] == key:
                del posts[post_id]
                return jsonify(id=post_id, key=key, timestamp=post['timestamp'])
            else:
                abort(403, description="Forbidden: Invalid key")
        else:
            abort(404, description="Post not found")

if __name__ == '__main__':
    app.run(debug=True)
