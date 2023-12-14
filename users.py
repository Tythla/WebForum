import os

class User:
    def __init__(self, user_id, key, username, real_name=None, avatar_icon=None):
        self.user_id = user_id
        self.key = key
        self.username = username  
        self.real_name = real_name  
        self.avatar_icon = avatar_icon

class UserManager:
    def __init__(self):
        self.users = {}
        self.user_id_counter = 0

    def create_user(self, username, real_name, avatar_icon):
        for user in self.users.values():
            if user.username == username:
                raise ValueError("Username already exists")

        self.user_id_counter += 1
        user_key = os.urandom(24).hex()
        new_user = User(self.user_id_counter, user_key, username, real_name, avatar_icon)
        self.users[self.user_id_counter] = new_user
        return new_user

    def validate_user(self, user_id, key):
        return user_id in self.users and self.users[user_id].key == key

    def get_user(self, user_id):
        return self.users.get(user_id)
