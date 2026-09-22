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

## 2026-09-21 — Finalisation sécurité et chat conversationnel

- Les routeurs `jobs`, `voice`, `agents` et `memory` exigent désormais un JWT Supabase valide.
- Les candidatures sont filtrées par `user_id` authentifié.
- `TELEGRAM_ALLOWED_USER_ID` est obligatoire et doit être strictement positif au démarrage.
- `005_opportunities_user_id.sql` ajoute la colonne propriétaire nullable et son index.
- `006_opportunities_backfill.sql` attribue les opportunités historiques sans propriétaire au premier utilisateur Supabase créé, puis impose `NOT NULL`. Cette règle de secours doit être contrôlée avant une exécution en production.
- `007_rls_policies.sql` active la RLS et applique `auth.uid() = user_id` aux tables applicatives. La politique `memories` est créée uniquement si cette table et sa colonne `user_id` existent.
- Le frontend transmet le JWT Supabase dans le header `Authorization`.
- Le chat charge les 10 derniers messages de `chat_history`, filtrés par `conversation_id` et `user_id`, puis les convertit en `HumanMessage` et `AIMessage` dans l’ordre chronologique.
- Les réponses Supabase sont vérifiées lors des insertions des messages utilisateur et assistant.

## 2026-09-21 — Décisions base de données et chat conversationnel

### Migration 006 — Backfill des opportunités

- Les lignes `opportunities.user_id IS NULL` sont attribuées au premier utilisateur Supabase existant.
- La migration échoue explicitement si aucun utilisateur Supabase n’existe.
- La colonne `opportunities.user_id` passe en `NOT NULL` après le backfill.

### Migration 007 — Politiques RLS

- Les tables ciblées sont `chat_history`, `knowledge_base`, `user_facts`, `job_applications`, `courses` et `opportunities`.
- Chaque table utilise `USING (auth.uid() = user_id)` et `WITH CHECK (auth.uid() = user_id)`.
- La table `memories` n’est pas ciblée : elle n’existe pas dans les migrations visibles et Mem0 utilise une collection externe.

### Chat conversationnel

- L’historique est filtré simultanément par `conversation_id` et `user_id`.
- Seuls les 10 derniers messages sont chargés.
- La requête Supabase utilise `desc=True`, puis les résultats sont inversés avec `reversed()` pour rétablir l’ordre chronologique.
- Les messages `user` sont convertis en `HumanMessage`.
- Les messages `assistant` sont convertis en `AIMessage`.
- Les messages `system` sont ignorés, car le prompt système est déjà défini dans l’agent.
- Les insertions du message utilisateur et de la réponse assistant vérifient explicitement `response.error`.
- Aucune transaction stricte n’est utilisée pour le MVP.

### Blocage frontend

- `npm.cmd install` reste bloqué sous OneDrive.
- Le lint TypeScript n’a pas pu être exécuté.
- La procédure recommandée est de fermer les terminaux et éditeurs utilisant `frontend/`, supprimer `node_modules` et `package-lock.json` s’ils existent, puis relancer :

```powershell
npm.cmd install --no-audit --no-fund --prefer-offline
```

- Si le blocage persiste, le dossier `frontend/` doit être copié temporairement vers `C:\Dev\jarvis-frontend\` afin d’y installer les dépendances et d’y lancer le lint.

## 2026-09-22 — Organisation définitive du workspace et leçons Git

### Emplacements

- `C:\dev\jarvis-gitdir` contient une copie de sûreté du répertoire `.git`. Il ne doit pas être modifié.
- `C:\dev\jarvis-repo` est le dépôt actif pour le backend, les migrations, la documentation, les commits et les pushs.
- `C:\dev\jarvis-frontend` est le workspace frontend pour `npm`, le développement et les validations Next.js.
- Le dépôt OneDrive est une sauvegarde passive du code source ; aucun Git actif ne doit y être utilisé.

### Règles opérationnelles

- Ne jamais lancer `npm`, `pnpm` ou `yarn` dans OneDrive.
- En fin de session, synchroniser le frontend avec `Sync-Jarvis`, vérifier le dépôt actif, puis commiter et pousser depuis `C:\dev\jarvis-repo`.
- Utiliser `git add` avec des fichiers explicitement contrôlés, jamais `git add -A` sans avoir vérifié `git status`.
- Vérifier la synchronisation avec `git rev-list --left-right --count HEAD...origin/main`.
- Avant un push, utiliser `git pull --rebase origin main` et ne jamais forcer le push sur `main`.
- Vérifier qu’aucun `node_modules`, `.next`, `dist`, `build`, `out` ou `coverage` n’est synchronisé vers OneDrive.

### `.gitignore` et commits

- La règle générique `lib/` ignorait potentiellement `frontend/lib/`.
- La règle correcte doit être ancrée à la racine :

```gitignore
/lib/
/lib64/
!frontend/lib/
!frontend/lib/**
```

- Le format de commit attendu est `type(scope): description courte`, avec un corps expliquant le pourquoi si nécessaire.
- Les types autorisés sont `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style` et `perf`.
- Les commits décrivant uniquement une manipulation technique, comme une copie de contournement, ne respectent pas cette convention.

### État de référence au 2026-09-22

- Sprints 1, 1.5 et 2 terminés.
- Tâches ouvertes : tests HTTP, test d’isolation multi-utilisateur, lint frontend, intégration vocale Telegram et complétion de `design.md` et `règles.md`.
- Commits poussés : `5835c1d` et `c391ae6`.