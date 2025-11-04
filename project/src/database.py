import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(ENV_PATH)

class Database:
    def __init__(self):
        # Permitir variables estándar y compatibilidad con NEXT_PUBLIC_* (usadas en proyectos web)
        url: str = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
        if not url or not key:
            raise RuntimeError(
                "Configuración de Supabase incompleta: asegúrate de definir SUPABASE_URL y SUPABASE_KEY en el archivo .env."
            )
        self.supabase: Client = create_client(url, key)
        self.current_user_id: Optional[str] = None

    def create_user(self, username: str, display_name: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.table("app_users").insert({
                "username": username,
                "display_name": display_name
            }).execute()

            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.table("app_users").select("*").eq("username", username).maybe_single().execute()
            return response.data
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def update_last_login(self, user_id: str) -> bool:
        try:
            self.supabase.table("app_users").update({
                "last_login": datetime.now(timezone.utc).isoformat()
            }).eq("id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating last login: {e}")
            return False

    def get_all_modules(self) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table("modules").select("*").order("order_index").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting modules: {e}")
            return []

    def get_module_by_id(self, module_id: int) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.table("modules").select("*").eq("id", module_id).maybe_single().execute()
            return response.data
        except Exception as e:
            print(f"Error getting module by id: {e}")
            return None

    def get_lessons_by_module(self, module_id: int) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table("lessons").select("*").eq("module_id", module_id).order("order_index").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting lessons: {e}")
            return []

    def get_lesson_by_id(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.table("lessons").select("*").eq("id", lesson_id).maybe_single().execute()
            return response.data
        except Exception as e:
            print(f"Error getting lesson: {e}")
            return None

    def get_quizzes_by_lesson(self, lesson_id: str) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table("quizzes").select("*").eq("lesson_id", lesson_id).order("order_index").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting quizzes: {e}")
            return []

    def get_user_progress(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table("user_progress").select("*").eq("user_id", user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return []

    def save_lesson_progress(self, user_id: str, lesson_id: str, completed: bool, score: int) -> bool:
        try:
            response = self.supabase.table("user_progress").upsert({
                "user_id": user_id,
                "lesson_id": lesson_id,
                "completed": completed,
                "score": score,
                "completed_at": datetime.now(timezone.utc).isoformat()
            }).execute()
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False

    def get_all_achievements(self) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table("achievements").select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting achievements: {e}")
            return []

    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table("user_achievements").select("*, achievements(*)").eq("user_id", user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting user achievements: {e}")
            return []

    def award_achievement(self, user_id: str, achievement_id: str) -> bool:
        try:
            existing = self.supabase.table("user_achievements").select("*").eq("user_id", user_id).eq("achievement_id", achievement_id).maybe_single().execute()

            if existing.data:
                return False

            self.supabase.table("user_achievements").insert({
                "user_id": user_id,
                "achievement_id": achievement_id
            }).execute()
            return True
        except Exception as e:
            print(f"Error awarding achievement: {e}")
            return False

    def get_module_completion(self, user_id: str, module_id: int) -> Dict[str, Any]:
        try:
            lessons = self.get_lessons_by_module(module_id)
            total_lessons = len(lessons)

            if total_lessons == 0:
                return {"completed": 0, "total": 0, "percentage": 0}

            lesson_ids = [lesson["id"] for lesson in lessons]

            progress = self.supabase.table("user_progress").select("*").eq("user_id", user_id).eq("completed", True).in_("lesson_id", lesson_ids).execute()

            completed_count = len(progress.data) if progress.data else 0
            percentage = int((completed_count / total_lessons) * 100)

            return {
                "completed": completed_count,
                "total": total_lessons,
                "percentage": percentage
            }
        except Exception as e:
            print(f"Error getting module completion: {e}")
            return {"completed": 0, "total": 0, "percentage": 0}
