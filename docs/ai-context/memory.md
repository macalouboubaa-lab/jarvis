# Mémoire du projet

## Décisions connues

- Les données doivent rester sur l'infrastructure Supabase propriétaire.
- PostgreSQL et pgvector sont utilisés pour la persistance et la recherche sémantique.
- Mem0 est connecté directement à PostgreSQL.
- La RLS est activée sur les tables.
- L'accès Telegram est restreint par `TELEGRAM_ALLOWED_USER_ID`.
- Le frontend est séparé du backend et communique avec une API FastAPI.

## Pourquoi ces choix

- Souveraineté des données : [À REMPLIR]
- Choix de Mem0/pgvector : [À REMPLIR]
- Choix de Telegram comme accès mobile : [À REMPLIR]

## Historique

- Le squelette full-stack, l'intégration Mem0 et le bot Telegram sont indiqués comme réalisés dans `docs/ROADMAP.md`.
- Historique détaillé des décisions : [À REMPLIR]

## Bugs connus et contournements

- [À REMPLIR]

## Points d'attention pour les futures sessions

- Vérifier les politiques RLS avant toute modification des accès aux données.
- Vérifier les variables d'environnement avant de lancer le backend, le frontend ou le bot.
- Mettre à jour ce fichier lorsqu'une décision d'architecture ou un contournement est adopté.

## 2026-09-21 — Audit technique initial

### Écarts entre documentation et implémentation

| Sujet | Documentation | Implémentation observée |
| --- | --- | --- |
| Chat Web | Présent | Présent |
| API FastAPI | Présente | Présente |
| Mem0 + pgvector | Présent | Présent dans le code |
| Bot Telegram texte | Présent | Présent |
| Notes vocales Telegram | Annoncées | Non visibles |
| ElevenLabs | Prévu / annoncé | Wrapper vide |
| Whisper | Prévu / annoncé | Non visible |
| Authentification Web | À préciser | Non visible sur les routeurs |
| RLS | Activée | Politiques concrètes non visibles |
| Historique conversationnel | Prévu | Lecture de l’historique absente |
| Scraping n8n | À faire | Non implémenté |
| Streaming ElevenLabs WebRTC | À faire | Non implémenté |

### Risques critiques identifiés

- L’authentification n’est pas démontrée sur les endpoints HTTP FastAPI.
- Les requêtes utilisent un `JARVIS_USER_ID` fixe au lieu de l’utilisateur authentifié.
- La RLS est activée, mais les politiques explicites d’accès ne sont pas présentes dans la migration inspectée.
- Les données pourraient donc être insuffisamment isolées et l’API pourrait être exposée à des accès non autorisés.

### Conclusion de l’audit

Jarvis dispose d’une bonne base d’architecture, mais n’est pas prêt pour la production. La priorité est de sécuriser l’API, d’assurer l’isolation par utilisateur et de compléter les politiques RLS avant toute exposition publique ou utilisation multi-utilisateur.