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

## 2026-10-21 — Audit technique

- Les routes métier appliquent des filtres `user_id`, mais le client Supabase backend utilise `SUPABASE_SERVICE_KEY`, qui contourne les politiques RLS : l’isolation dépend donc de chaque chemin applicatif.
- Risque multi-utilisateur confirmé pour les cours : `courses.name` est globalement `UNIQUE` et l’outil fait `upsert(..., on_conflict="name")`; un conflit peut remplacer le `user_id` de la ligne existante.
- `docker-compose.yml` contient des mots de passe par défaut et publie les ports PostgreSQL/n8n ; ne pas exposer cette configuration telle quelle.
- Le statut voix est constant et le bouton micro du frontend enregistre sans envoyer ni transcrire le média. Les fonctionnalités voix annoncées ne sont pas complètes.
- `AgentExecutor` est configuré avec `verbose=True`; les outils renvoient les exceptions sous forme de chaîne. Examiner les risques de journalisation et d’exposition d’informations.
- Aucun test, CI, Dockerfile ou lockfile n’a été trouvé. Les dépendances sont épinglées seulement côté Python ; l’audit CVE n’a pas pu s’exécuter faute de `pip-audit`, Node et npm dans l’environnement.
- Priorités de correction consignées dans `tasks.md` : sécuriser Compose et l’upsert cross-user avant exposition publique, puis tests d’isolation, protections contre les abus et fiabilisation des intégrations.

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

## 2026-10-22 — État opérationnel du devcontainer

- `.devcontainer/devcontainer.json` est lisible comme JSON strict et configure `mcr.microsoft.com/devcontainers/universal:2-linux`, Docker-in-Docker et `runArgs` privilégiés.
- Malgré cette configuration, la session examinée fonctionne toujours sous Alpine et expose `CapEff=0000000000000000`.
- La session ne dispose ni de la commande `docker`, ni de `/var/run/docker.sock`, ni d’un outil CLI VS Code permettant de lancer « Rebuild Without Cache ». Le rebuild doit être lancé depuis l’interface VS Code.
- Après le rebuild, vérifier l’OS, `CapEff`, `docker info`, puis lancer `docker compose up --build backend`. Le fichier `.env` est présent ; ne pas afficher son contenu.

## 2026-10-22 — Migration Next.js 15, build intermédiaire

- La migration intermédiaire a installé Next.js et `eslint-config-next` 15.5.28, React et React DOM 19.3.1, `@types/react` et `@types/react-dom` 19.3.0.
- `lucide-react` a été mis à jour de 0.395.0 à 1.61.0 pour résoudre son peer dependency React 19.
- L’absence de `frontend/app/not-found.tsx` a été corrigée avec une page 404 minimale. Après suppression du cache `frontend/.next`, `npm run build` a réussi et généré les routes statiques.
- Aucun commit n’a été créé. La vérification manuelle de l’interface avec `npm run dev` reste en attente.
- npm signale 11 vulnérabilités (3 modérées, 8 hautes). Le build avertit aussi que plusieurs lockfiles existent et choisit la racine du dépôt ; à examiner avant migration finale.

## 2026-10-22 — Migration Next.js 16.4.2

- Next.js et `eslint-config-next` sont en 16.4.2 ; React et React DOM sont en 19.3.1. La compatibilité Next 16 a été vérifiée avec Node 24.18.1 (Next exige Node >=20.9).
- Aucun usage de `params`, `searchParams`, `cookies()` ou `headers()` n'a été trouvé dans `frontend/app/`.
- Le lockfile racine sans manifeste racine a été supprimé ; le lockfile frontend reste la référence.
- `eslint-config-next` et ESLint sont configurés en dépendances de développement. ESLint 9 utilise la configuration flat ; le script lint appelle `eslint .`.
- La configuration `frontend/postcss.config.mjs` active Tailwind 3 et Autoprefixer pour Turbopack. Le build Next 16 passe sans avertissements CSS.
- `npm audit --omit=dev` rapporte 0 vulnérabilité. L'audit complet signale encore 9 vulnérabilités de développement (7 hautes et 2 modérées), notamment via ESLint/Tailwind.
- `npm run lint` révèle 3 erreurs et 1 avertissement préexistants dans `app/chat/page.tsx`, `app/jobs/page.tsx`, `app/memory/page.tsx` et `components/ChatInput.tsx`. Aucun code métier n'a été modifié.
- Le serveur Next 16 est actif sur le port 3001 ; `/chat` répond HTTP 200. La revue visuelle humaine reste à faire.
- Next 16 a généré `frontend/AGENTS.md` au démarrage de `next dev`; son contenu précise qu'il est réécrit automatiquement.
- Aucun commit n'a été créé.

## 2026-10-22 — Correctif d'hydratation ChatBubble

- L'utilisateur a validé visuellement l'interface après la migration et a signalé un décalage de locale/timezone dans l'heure de `ChatBubble`.
- `suppressHydrationWarning` est appliqué au seul `<span>` qui affiche l'heure ; le contenu et le comportement métier ne changent pas.
- Validation après correctif : `npm run build` réussi sous Next.js 16.4.2 et `npm audit --omit=dev` rapporte 0 vulnérabilité runtime.
- L'audit complet des dépendances de développement reste distinct et signale encore des vulnérabilités ; le commit ne doit pas être décrit comme supprimant ces vulnérabilités de développement.