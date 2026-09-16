from langchain_core.tools import tool
from config import settings
from database import supabase

@tool
def update_course(course_name: str, progress_percentage: int, notes: str = "") -> str:
    """Met à jour l'avancement d'un cours ou veille dans Supabase."""
    try:
        data = {
            "name": course_name,
            "progress": progress_percentage,
            "notes": notes,
            "user_id": settings.JARVIS_USER_ID
        }
        supabase.table("courses").upsert(data, on_conflict="name").execute()
        return f"Cours '{course_name}' mis à jour à {progress_percentage}%."
    except Exception as e:
        return f"Erreur mise à jour cours : {str(e)}"
