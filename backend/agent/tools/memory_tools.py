from langchain_core.tools import tool
from agent.context import current_user_id
from memory.mem0_client import mem0_instance

@tool
def remember(fact: str) -> str:
    """Mémorise un fait important ou une préférence concernant l'utilisateur dans sa mémoire Supabase."""
    try:
        user_id = current_user_id.get()
        if user_id is None:
            return "Erreur lors de la mémorisation : utilisateur non authentifié."
        mem0_instance.add(
            fact,
            user_id=user_id,
            metadata={"source": "agent_action"}
        )
        return f"Information mémorisée avec succès dans Supabase : '{fact}'"
    except Exception as e:
        return f"Erreur lors de la mémorisation : {str(e)}"

@tool
def recall(query: str) -> str:
    """Recherche des souvenirs, faits ou préférences précédemment enregistrés sur l'utilisateur."""
    try:
        user_id = current_user_id.get()
        if user_id is None:
            return "Erreur lors du rappel de mémoire : utilisateur non authentifié."
        results = mem0_instance.search(query, user_id=user_id, limit=4)
        if not results:
            return "Aucun souvenir trouvé correspondant à cette requête."
        formatted = "\n".join([f"- {r.get('memory', '')}" for r in results])
        return f"Souvenirs retrouvés :\n{formatted}"
    except Exception as e:
        return f"Erreur lors du rappel de mémoire : {str(e)}"
