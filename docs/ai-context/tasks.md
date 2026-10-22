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

## Audit technique — 2026-10-21

### Priorité P0 — avant toute exposition publique

- [ ] Supprimer les mots de passe codés en dur dans `docker-compose.yml` et ne pas publier PostgreSQL/n8n sans authentification et filtrage réseau adaptés.
- [ ] Corriger l’upsert des cours : la contrainte globale `courses.name UNIQUE` et `ON CONFLICT (name)` peuvent transférer une ligne d’un utilisateur à un autre avec la clé `service_role`.
- [ ] Ajouter des tests d’authentification et d’isolation multi-utilisateur, notamment sur les outils agent et les conflits d’upsert.

### Priorité P1 — robustesse et exploitation

- [ ] Remplacer les réponses vocales fictives et implémenter le cycle audio de bout en bout (capture, transfert, transcription et synthèse selon les fonctionnalités annoncées).
- [ ] Ajouter des limites de débit, limites de taille/durée d’entrée et timeouts pour les appels externes coûteux.
- [ ] Éviter les appels Supabase synchrones dans les routes async ou les exécuter hors boucle d’événements.
- [ ] Désactiver `AgentExecutor(verbose=True)` en production et éviter de retourner les exceptions d’outils au modèle/utilisateur.
- [ ] Ajouter CI, tests backend/frontend/migrations, verrouillage des dépendances et scans CVE reproductibles.

### Constat de validation

- Aucun fichier de test, workflow CI, Dockerfile ni lockfile de dépendances n’a été trouvé lors de l’audit.
- Le scanner `pip-audit` et Node/npm ne sont pas disponibles dans l’environnement d’audit ; les CVE n’ont donc pas été vérifiées.

## 2026-10-22 — Rebuild du devcontainer

- [x] Vérifier que `.devcontainer/devcontainer.json` est du JSON valide.
- [ ] Rebuild du devcontainer sans cache depuis VS Code.
- [ ] Après rebuild, vérifier que le conteneur utilise l’image Ubuntu attendue et que `CapEff` est non nul.
- [ ] Vérifier l’accès à Docker et lancer `docker compose up --build backend`.

### Blocage constaté

- La session actuelle tourne encore sous Alpine (`/etc/os-release`), avec `CapEff=0000000000000000`.
- Aucun binaire `docker`, socket `/var/run/docker.sock` ou outil CLI VS Code utilisable pour reconstruire le devcontainer n’est disponible dans cette session.
- Le rebuild et le lancement Compose doivent être effectués depuis VS Code après réouverture/reconnexion au conteneur.

## 2026-10-22 — Décision : Docker abandonné dans Codespaces

### Problème

- Codespaces free tier bloque `--privileged` (`CapEff: 0`).
- Alpine est incompatible avec la feature `docker-in-docker:2`.
- Le rebuild tente Ubuntu, mais reste sur Alpine (fallback).

### Décision

- ✅ Plan B : lancer l'app en direct (`uvicorn` + `next dev`) dans Codespaces.
- ✅ Dockerfiles et Compose conservés pour CI (Jour 4) et production.
- ⏸️ Tests Docker en local à faire avec Docker Desktop si besoin.

### Ce qui n'est PAS affecté

- Le code applicatif : aucune modification.
- Le Compose A-cloud : toujours valide (`config --quiet` passe).
- Les Dockerfiles : prêts pour la CI.
- La décision Supabase-first : inchangée.

### Prochaines étapes

- [ ] Lancer le backend en direct (`uvicorn`).
- [ ] Lancer le frontend en direct (`npm run dev`).
- [ ] Ouvrir l'interface via les ports Codespaces.
- [ ] Jour 3 (pre-commit) : à faire normalement.
- [ ] Jour 4 (CI) : utiliser Docker Desktop en local pour tester, ou GitHub Actions*.

## 2026-10-22 — Migration Next.js 15 : premier build réussi

- [x] Installer Next.js 15, `eslint-config-next` 15, React 19, React DOM 19 et les types React 19.
- [x] Mettre à jour `lucide-react` pour résoudre le conflit de peer dependencies React 19.
- [x] Ajouter `frontend/app/not-found.tsx` et reconstruire après suppression du cache `.next`.
- [x] `npm run build` passe sur Next.js 15.5.28 ; les routes statiques sont générées.
- [ ] Valider `npm run dev` et l'interface dans le navigateur avant tout commit.
- [ ] Examiner l'avertissement de racine workspace causé par plusieurs lockfiles.
- [ ] Traiter les vulnérabilités rapportées par npm avant la validation de sécurité finale.

### État des changements

- Aucun commit créé.
- `npm install` signale encore 11 vulnérabilités : 3 modérées et 8 hautes.
- `next`, `react` et `react-dom` sont en 15.5.28, 19.3.1 et 19.3.1 ; les types React sont en 19.3.0.

## 2026-10-22 — Migration Next.js 16

- [x] Vérifier qu'aucune utilisation de `params`, `searchParams`, `cookies()` ou `headers()` n'est présente dans `frontend/app/`.
- [x] Supprimer le lockfile racine orphelin (`package-lock.json` sans `package.json` racine).
- [x] Migrer vers Next.js et `eslint-config-next` 16.4.2, React et React DOM 19.3.1.
- [x] Installer ESLint 9 et configurer ESLint flat config ; remplacer `next lint` par `eslint .`.
- [x] Ajouter la configuration PostCSS manquante pour que Tailwind soit traité sous Turbopack.
- [x] `npm run build` passe sous Next.js 16.4.2 sans avertissements CSS.
- [x] `npm audit --omit=dev` : 0 vulnérabilité.
- [x] `npm run dev` répond HTTP 200 sur `/chat` au port 3001.
- [ ] Vérification visuelle manuelle par l'utilisateur dans le navigateur.
- [ ] Examiner les vulnérabilités des dépendances de développement et corriger les erreurs lint préexistantes sans modifier le code métier sans validation.

### État des changements

- Aucun commit créé.
- `npm run lint` détecte 3 erreurs et 1 avertissement dans des fichiers métier existants ; ils n'ont pas été modifiés.
- Next.js 16 a généré `frontend/AGENTS.md` automatiquement ; le fichier indique qu'il est réécrit par `next dev`.
- Le serveur de développement reste démarré sur le port 3001 pour la vérification visuelle.

## 2026-10-22 — Correctif d'hydratation et validation finale

- [x] Ajouter `suppressHydrationWarning` sur l'horodatage dans `frontend/components/ChatBubble.tsx`.
- [x] Rejouer `npm run build` sur Next.js 16.4.2 : succès.
- [x] Rejouer `npm audit --omit=dev` : 0 vulnérabilité runtime.
- [x] Vérification visuelle de l'interface effectuée par l'utilisateur.
- [ ] Examiner séparément les vulnérabilités restantes dans les dépendances de développement.
