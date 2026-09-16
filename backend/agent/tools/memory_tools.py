from langchain_core.tools import tool
from config import settings
from memory.mem0_client import mem0_instance

@tool
def remember(fact: str) -> str:
    """Mémorise un fait important ou une préférence concernant l'utilisateur dans sa mémoire Supabase."""
    try:
        mem0_instance.add(
            fact,
            user_id=settings.JARVIS_USER_ID,
            metadata={"source": "agent_action"}
        )
        return f"Information mémorisée avec succès dans Supabase : '{fact}'"
    except Exception as e:
        return f"Erreur lors de la mémorisation : {str(e)}"

@tool
def recall(query: str) -> str:
    """Recherche des souvenirs, faits ou préférences précédemment enregistrés sur l'utilisateur."""
    try:
        results = mem0_instance.search(query, user_id=settings.JARVIS_USER_ID, limit=4)
        if not results:
            return "Aucun souvenir trouvé correspondant à cette requête."
        formatted = "\n".join([f"- {r.get('memory', '')}" for r in results])
        return f"Souvenirs retrouvés :\n{formatted}"
    except Exception as e:
        return f"Erreur lors du rappel de mémoire : {str(e)}"
