# Tâches et progrès — Projet Jarvis

## 🎯 Sprint 1 — Sécuriser l'API (Statut : ✅ 100% Terminé)

### ✅ Terminé

- [x] Authentification Supabase (`get_current_user`, JWT HS256).
- [x] Configuration : `JARVIS_USER_ID` supprimé, `SUPABASE_JWT_SECRET` ajouté.
- [x] Protection de `chat.py`, `jobs.py`, `voice.py`, `agents.py`, `memory.py`.
- [x] Propagation du `user_id` via `ContextVar` dans l’agent LangChain.
- [x] Migration `005` : ajout de `opportunities.user_id` (nullable).
- [x] Masquage des erreurs dans `chat.py` (logger + message générique).
- [x] Frontend `api.ts` : injection du header `Authorization: Bearer <token>`.

## 🎯 Sprint 1.5 — Finalisation Sécurité (Statut : ✅ Terminé)

### ✅ Terminé

- [x] **Migration `006`** : backfill des `user_id` NULL dans `opportunities` et passage en `NOT NULL`.
- [x] **Migration `007`** : activation RLS sur `chat_history`, `knowledge_base`, `user_facts`, `job_applications`, `courses`, `opportunities`, avec politiques `auth.uid() = user_id`.
- [x] **Telegram** : `TELEGRAM_ALLOWED_USER_ID` obligatoire et validé au démarrage (`gt=0`).
- [x] **Validation Python** : `ast.parse` OK sur 7 fichiers.
- [x] **Validation sécurité** : aucune occurrence de `JARVIS_USER_ID` ni `detail=str(e)` dans `backend/`.

### 🚧 Blocage actuel

- [ ] **Frontend Lint** : l’installation de npm a échoué, bloquée sous OneDrive. Les dépendances ne sont pas installées (`node_modules` absent) et le lint TypeScript n’a pas pu être exécuté.

## 💬 Sprint 2 — Chat Conversationnel (Statut : ✅ Terminé)

### ✅ Terminé

- [x] Conversion Supabase vers LangChain (`to_langchain_messages` dans `core.py`).
- [x] Chargement de l’historique dans `chat.py` : 10 derniers messages filtrés par `conversation_id` et `user_id`.
- [x] Inversion chronologique avec `reversed()`.
- [x] Appel de `ask_jarvis(..., history=history)` avec typage `list[BaseMessage]`.
- [x] Persistance vérifiée : les insertions Supabase contrôlent explicitement les erreurs avec `if response.error`.

### 🚧 À faire — Tests et validation

- [ ] Tests HTTP : requête sans token → `401`, avec token → `200`.
- [ ] Test d’isolation entre deux utilisateurs.
- [ ] Gestion des notes vocales Telegram.
- [ ] Résolution du blocage `npm install` et exécution du lint frontend.

## Priorité 2 — Voix

- [ ] Implémenter la réception et le téléchargement des notes vocales Telegram.
- [ ] Intégrer la transcription Whisper.
- [ ] Intégrer réellement la synthèse vocale ElevenLabs.
- [ ] Ajouter la réponse audio Telegram lorsque le flux est disponible.
- [ ] Remplacer le statut vocal fictif par une vérification réelle de configuration et de disponibilité.
- [ ] Implémenter ou replanifier explicitement le streaming ElevenLabs WebRTC.

## Priorité 3 — Qualité et exploitation

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

- Dernière mise à jour : 2026-09-21 — Sprint 1.5 et Sprint 2 implémentés, validations restantes documentées.
- Responsable : [À REMPLIR]
