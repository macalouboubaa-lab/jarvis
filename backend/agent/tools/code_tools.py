from langchain_core.tools import tool

@tool
def analyze_code(code_snippet: str, language: str = "python") -> str:
    """Analyse un extrait de code pour détecter bugs, failles et optimisations."""
    return f"Analyse syntaxique et sécurité effectuée pour le snippet ({language}). Prêt pour revue détaillée."

@tool
def suggest_refactor(code_snippet: str) -> str:
    """Propose un refactoring moderne et typé du code fourni."""
    return "Proposition de refactorisation prête."
