import os

class User:
    def __init__(self, user_id, key):
        self.user_id = user_id
        self.key = key

class UserManager:
    def __init__(self):
        self.users = {}
        self.user_id_counter = 0

    def create_user(self):
        self.user_id_counter += 1
        user_key = os.urandom(24).hex()
        new_user = User(self.user_id_counter, user_key)
        self.users[self.user_id_counter] = new_user
        return new_user

    def validate_user(self, user_id, key):
        return user_id in self.users and self.users[user_id].key == key

    def get_user(self, user_id):
        return self.users.get(user_id)
