from flask import Flask, request, jsonify, abort
import datetime
import os
import threading
from users import UserManager
from datetime import datetime

app = Flask(__name__)

posts = {}
post_id = 0
user_manager = UserManager()
lock = threading.Lock()
admin_key = "admin_key"

@app.route('/create_moderator', methods=['POST'])
def create_moderator():
    if request.headers.get('Admin-Key') != admin_key:
        abort(403, description="Unauthorized")

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

@app.route('/posts', methods=['GET'])
def get_posts_by_date():
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        if start:
            start = datetime.fromisoformat(start)
        if end:
            end = datetime.fromisoformat(end)
    except ValueError:
        abort(400, description="Invalid date format. Use ISO 8601 format.")

    filtered_posts = []
    with lock:
        for post in posts.values():
            post_time = datetime.fromisoformat(post['timestamp'])
            if (not start or post_time >= start) and (not end or post_time <= end):
                filtered_posts.append(post)

    return jsonify(filtered_posts)

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
        if any(user.mod_key == key and user.is_moderator for user in user_manager.users.values()):
            del posts[post_id]
            return jsonify(status="Post deleted by moderator")
        if post['key'] == key or (post.get('user_id') and user_manager.validate_user(post['user_id'], key)):
            del posts[post_id]
            return jsonify(id=post_id, key=key, timestamp=post['timestamp'])
        else:
            abort(403, description="Forbidden: Invalid key")

if __name__ == '__main__':
    app.run(debug=True)
