import unittest
import json
from app import app
from users import UserManager, User


class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()

    def test_create_user(self):
        # Test user creation
        user = self.user_manager.create_user("testuser", "Test User")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_create_moderator(self):
        # Test moderator creation
        mod = self.user_manager.create_moderator("moduser", "Mod User")
        self.assertIsNotNone(mod)
        self.assertEqual(mod.username, "moduser")
        self.assertTrue(mod.is_moderator)

    def test_user_validation(self):
        # Test user validation
        user = self.user_manager.create_user("validuser", "Valid User")
        is_valid = self.user_manager.validate_user(user.user_id, user.key)
        self.assertTrue(is_valid)

        is_invalid = self.user_manager.validate_user(user.user_id, "wrongkey")
        self.assertFalse(is_invalid)

    def test_get_user(self):
        # Test retrieving a user
        user = self.user_manager.create_user("existinguser", "Existing User")
        retrieved_user = self.user_manager.get_user(user.user_id)
        self.assertEqual(retrieved_user, user)

        retrieved_user = self.user_manager.get_user(
            9999)  # Assuming this ID doesn't exist
        self.assertIsNone(retrieved_user)


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.user_manager = UserManager()

    def test_create_user_endpoint(self):
        # Test the create user endpoint
        response = self.app.post('/user', json={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')

    def test_create_moderator_endpoint(self):
        response = self.app.post('/create_moderator',
                                headers={'Admin-Key': 'admin_key'},
                                json={'username': 'newmod', 'real_name': 'New Mod'})
        self.assertEqual(response.status_code, 201)

    def test_post_creation_endpoint(self):
        # Test post creation
        post_data = {'msg': 'This is a test post'}
        response = self.app.post('/post', json=post_data)
        self.assertEqual(response.status_code, 200)

    def test_post_read_endpoint(self):
        # Test reading a post
        # Create a post then test reading that post
        response = self.app.get('/post/1')  # Assuming a post with ID 1
        self.assertEqual(response.status_code, 200)

    def test_post_delete_endpoint(self):
        # Create a post and get its ID and key
        post_data = {'msg': 'Test Post for Deletion'}
        create_response = self.app.post('/post', json=post_data)
        post_id = create_response.json['id']
        key = create_response.json['key']

        # Delete the post
        delete_url = f'/post/{post_id}/delete/{key}'
        response = self.app.delete(delete_url)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
