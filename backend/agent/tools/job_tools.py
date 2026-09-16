from langchain_core.tools import tool
from database import supabase

@tool
def search_jobs(keywords: str, location: str = "Télétravail") -> str:
    """Recherche des offres d'emploi ou opportunités dans la base souveraine Supabase."""
    try:
        response = supabase.table("opportunities") \
            .select("title, company, location, url, status") \
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
        data = {"job_url": job_id, "status": "postule", "notes": notes}
        supabase.table("job_applications").insert(data).execute()
        return f"Candidature pour {job_id} marquée comme envoyée."
    except Exception as e:
        return f"Erreur : {str(e)}"
