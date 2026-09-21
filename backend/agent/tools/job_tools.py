from langchain_core.tools import tool
from agent.context import current_user_id
from database import supabase

@tool
def search_jobs(keywords: str, location: str = "Télétravail") -> str:
    """Recherche des offres d'emploi ou opportunités dans la base souveraine Supabase."""
    try:
        user_id = current_user_id.get()
        if user_id is None:
            return "Erreur de recherche d'emploi : utilisateur non authentifié."
        response = supabase.table("opportunities") \
            .select("title, company, location, url, status") \
            .eq("user_id", user_id) \
            .ilike("title", f"%{keywords}%") \
            .limit(5) \
            .execute()
        items = response.data
        if not items:
            return f"Aucune offre enregistrée trouvée pour '{keywords}' à '{location}'."
        summary = "\n".join([f"- {j['title']} chez {j['company']} ({j['location']})" for j in items])
        return f"Offres trouvées :\n{summary}"
    except Exception as e:
        return f"Erreur de recherche d'emploi : {str(e)}"

@tool
def apply_job(job_id: str, notes: str = "") -> str:
    """Enregistre une candidature dans le suivi de candidatures Supabase."""
    try:
        user_id = current_user_id.get()
        if user_id is None:
            return "Erreur : utilisateur non authentifié."
        data = {
            "job_url": job_id,
            "status": "postule",
            "notes": notes,
            "user_id": user_id,
        }
        supabase.table("job_applications").insert(data).execute()
        return f"Candidature pour {job_id} marquée comme envoyée."
    except Exception as e:
        return f"Erreur : {str(e)}"
