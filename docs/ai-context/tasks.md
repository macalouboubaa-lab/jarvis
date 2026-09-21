# Tâches et progrès

## État actuel

- [x] Mettre en place le squelette FastAPI et Next.js.
- [x] Intégrer Mem0 avec pgvector.
- [x] Ajouter le bot Telegram texte.
- [x] Ajouter les migrations SQL et l’activation initiale de RLS.
- [x] Ajouter l’interface de chat Web.
- [x] Ajouter l’agent LangChain et ses outils métier.
- [x] Ajouter les six fichiers de contexte IA.

## Priorité 0 — Sécuriser l’API

- [~] Ajouter une authentification Supabase obligatoire sur tous les endpoints HTTP.
- [ ] Remplacer `JARVIS_USER_ID` fixe par l’identité authentifiée de la requête.
- [ ] Isoler toutes les lectures et écritures par `user_id` authentifié.
- [ ] Définir les politiques RLS explicites pour chaque table.
- [ ] Vérifier et rendre obligatoire la restriction `TELEGRAM_ALLOWED_USER_ID`.
- [ ] Remplacer l’exposition de `str(e)` par des messages génériques côté client et des logs serveur contrôlés.
- [ ] Vérifier qu’aucun secret n’est exposé dans les réponses ou les logs.

## Priorité 1 — Chat conversationnel

- [ ] Charger l’historique correspondant à `conversation_id` avant l’appel de l’agent.
- [ ] Convertir l’historique persisté en messages LangChain.
- [ ] Ajouter une limite de taille du contexte et une stratégie de résumé.
- [ ] Gérer proprement les erreurs et les statuts de traitement du chat.
- [ ] Vérifier la persistance cohérente des messages utilisateur et assistant.

## Priorité 2 — Voix

- [ ] Implémenter la réception et le téléchargement des notes vocales Telegram.
- [ ] Intégrer la transcription Whisper.
- [ ] Intégrer réellement la synthèse vocale ElevenLabs.
- [ ] Ajouter la réponse audio Telegram lorsque le flux est disponible.
- [ ] Remplacer le statut vocal fictif par une vérification réelle de configuration et de disponibilité.
- [ ] Implémenter ou replanifier explicitement le streaming ElevenLabs WebRTC.

## Priorité 3 — Qualité & exploitation

- [ ] Ajouter des tests backend pour `/health`, `/api/chat`, `/api/memory` et les autres routeurs.
- [ ] Ajouter des tests pour les outils de l’agent et le filtrage Telegram.
- [ ] Ajouter des tests frontend ciblés pour le client API et le chat.
- [ ] Définir et configurer le lint et le formatage Python.
- [ ] Vérifier le lint TypeScript et le build frontend.
- [ ] Ajouter une CI pour les validations backend, frontend et migrations.
- [ ] Ajouter des logs structurés sans secrets.
- [ ] Ajouter une observabilité minimale et une limitation de débit.
- [ ] Valider les migrations Supabase dans un environnement de test.
- [ ] Compléter les critères d’acceptation produit.

## Vérification

- Dernière mise à jour : 2026-09-21 — audit technique initial.
- Responsable : [À REMPLIR]