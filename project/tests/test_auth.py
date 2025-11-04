import unittest

from src.auth import AuthManager


class FakeDatabase:
    def __init__(self, users=None):
        self.users = users or {}
        self.current_user_id = None

    def get_user_by_username(self, username):
        return self.users.get(username)

    def update_last_login(self, user_id: str) -> bool:
        # Simular que la actualización siempre funciona
        return True


class TestAuthManager(unittest.TestCase):
    def test_login_rejects_short_username(self):
        db = FakeDatabase()
        auth = AuthManager(db)
        ok, msg = auth.login("ab")
        self.assertFalse(ok)
        self.assertIn("al menos 3", msg)

    def test_login_user_not_found(self):
        db = FakeDatabase(users={})
        auth = AuthManager(db)
        ok, msg = auth.login("usuario")
        self.assertFalse(ok)
        self.assertIn("no encontrado", msg)

    def test_login_success_sets_current_user(self):
        user = {"id": "u-123", "username": "alumno", "display_name": "Alumno"}
        db = FakeDatabase(users={"alumno": user})
        auth = AuthManager(db)

        ok, msg = auth.login("alumno")
        self.assertTrue(ok)
        self.assertIn("exitoso", msg)
        self.assertEqual(auth.current_user, user)
        self.assertEqual(db.current_user_id, user["id"])


if __name__ == "__main__":
    unittest.main()