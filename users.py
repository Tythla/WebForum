import os

class User:
    def __init__(self, user_id, key, username, is_moderator=False, mod_key=None, real_name=None):
        self.user_id = user_id
        self.key = key
        self.username = username
        self.is_moderator = is_moderator
        self.mod_key = mod_key if is_moderator else None
        self.real_name = real_name

class UserManager:
    def __init__(self):
        self.users = {}
        self.user_id_counter = 0

    def create_moderator(self, username, real_name):
        self.user_id_counter += 1
        user_key = os.urandom(24).hex()
        mod_key = os.urandom(24).hex()
        new_user = User(self.user_id_counter, user_key, username, True, mod_key, real_name)
        self.users[self.user_id_counter] = new_user
        return new_user

    def create_user(self, username, real_name):
        for user in self.users.values():
            if user.username == username:
                raise ValueError("Username already exists")

        self.user_id_counter += 1
        user_key = os.urandom(24).hex()
        new_user = User(self.user_id_counter, user_key, username, real_name)
        self.users[self.user_id_counter] = new_user
        return new_user

    def validate_user(self, user_id, key):
        return user_id in self.users and self.users[user_id].key == key

    def get_user(self, user_id):
        return self.users.get(user_id)
