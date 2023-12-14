from flask import Flask, request, jsonify, abort
import datetime
import os
import threading
from users import UserManager

app = Flask(__name__)

posts = {}
post_id = 0
user_manager = UserManager()
lock = threading.Lock()

@app.route('/user', methods=['POST'])
def create_user():
    content = request.json
    username = content.get('username')
    real_name = content.get('real_name', None)
    avatar_icon = content.get('avatar_icon', None)

    if not username:
        abort(400, description="Username is required")

    new_user = user_manager.create_user(username, real_name, avatar_icon)
    return jsonify(user_id=new_user.user_id, user_key=new_user.key, username=new_user.username)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_metadata(user_id):
    user = user_manager.get_user(user_id)
    if not user:
        abort(404, description="User not found")

    return jsonify(user_id=user.user_id, username=user.username, real_name=user.real_name, avatar_icon=user.avatar_icon)

@app.route('/user/<int:user_id>', methods=['PUT'])
def edit_user_metadata(user_id):
    content = request.json
    user_key = content.get('user_key')
    new_real_name = content.get('real_name')
    new_avatar_icon = content.get('avatar_icon')

    if not user_manager.validate_user(user_id, user_key):
        abort(403, description="Invalid user ID or key")

    user = user_manager.get_user(user_id)
    if new_real_name:
        user.real_name = new_real_name
    if new_avatar_icon:
        user.avatar_icon = new_avatar_icon

    return jsonify(user_id=user.user_id, username=user.username, real_name=user.real_name, avatar_icon=user.avatar_icon)

@app.route('/post', methods=['POST'])
def create_post():
    global post_id
    content = request.json

    if not content or 'msg' not in content or not isinstance(content['msg'], str):
        return jsonify(error="Bad Request"), 400
    
    user_id = content.get('user_id')
    user_key = content.get('user_key')

    if user_id and user_key:
        with lock:
            if user_manager.validate_user(user_id, user_key):
                post_id += 1
                key = os.urandom(24).hex()
                timestamp = datetime.datetime.utcnow().isoformat()
                post = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': content['msg'], 'user_id': user_id}
                posts[post_id] = post
                return jsonify(post)
            else:
                abort(403, description="Invalid user ID or key")

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
            user_id = post.get('user_id')
            user_data = None
            if user_id:
                user = user_manager.get_user(user_id)
                if user:
                    user_data = {'user_id': user.user_id, 'username': user.username}
            return jsonify(id=post['id'], timestamp=post['timestamp'], msg=post['msg'], user=user_data)
        else:
            abort(404, description="Post not found")

@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    with lock:
        if post_id not in posts:
            abort(404, description="Post not found")

        post = posts[post_id]
        # Check if the key is either the post's key or the user's key
        if post['key'] == key or (post.get('user_id') and user_manager.validate_user(post['user_id'], key)):
            del posts[post_id]
            return jsonify(id=post_id, key=key, timestamp=post['timestamp'])
        else:
            abort(403, description="Forbidden: Invalid key")

if __name__ == '__main__':
    app.run(debug=True)
