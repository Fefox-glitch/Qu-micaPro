from typing import Optional, Dict, Any
from src.database import Database

class AuthManager:
    def __init__(self, database: Database):
        self.db = database
        self.current_user: Optional[Dict[str, Any]] = None

    def login(self, username: str) -> tuple[bool, str]:
        if not username or len(username.strip()) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"

        user = self.db.get_user_by_username(username)

        if user:
            self.current_user = user
            self.db.update_last_login(user["id"])
            self.db.current_user_id = user["id"]
            return True, "Inicio de sesión exitoso"
        else:
            return False, "Usuario no encontrado"

    def register(self, username: str, display_name: str) -> tuple[bool, str]:
        if not username or len(username.strip()) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"

        if not display_name or len(display_name.strip()) < 2:
            return False, "El nombre para mostrar debe tener al menos 2 caracteres"

        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return False, "Este nombre de usuario ya está en uso"

        new_user = self.db.create_user(username, display_name)
        if new_user:
            self.current_user = new_user
            self.db.current_user_id = new_user["id"]
            return True, "Registro exitoso"
        else:
            return False, "Error al crear usuario"

    def logout(self):
        self.current_user = None
        self.db.current_user_id = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        return self.current_user

    def get_current_user_id(self) -> Optional[str]:
        if self.current_user:
            return self.current_user["id"]
        return None
