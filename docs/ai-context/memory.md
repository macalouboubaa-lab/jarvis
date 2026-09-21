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