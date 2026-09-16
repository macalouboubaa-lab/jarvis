from langchain_core.tools import tool

@tool
def read_emails(limit: int = 5) -> str:
    """Consulte les derniers e-mails non traités (via intégration webhook n8n)."""
    return "Aucun e-mail urgent en attente dans la file n8n."

@tool
def draft_reply(recipient: str, subject: str, body: str) -> str:
    """Rédige un brouillon d'e-mail souverain."""
    return f"Brouillon préparé pour {recipient} avec pour objet '{subject}'."
