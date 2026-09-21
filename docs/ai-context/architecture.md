# Architecture du projet

## Vue d'ensemble

```text
Utilisateur (Web Next.js / Mobile Telegram)
                    |
                    v
              FastAPI Core
         +---------+----------+
         v                    v
   LangChain Agent       Mem0 Memory
         |                    |
         +---------+----------+
                   v
     Supabase (PostgreSQL + pgvector)
```

## Stack

### Frontend

- Next.js `14.2.4`.
- React `18.3.1`.
- TypeScript `5.4.5`.
- Tailwind CSS `3.4.4`.
- `lucide-react`, `clsx`, `tailwind-merge`.
- Client Supabase via `@supabase/supabase-js`.

### Backend

- Python avec FastAPI `0.111.0` et Uvicorn.
- Pydantic et `pydantic-settings` pour la configuration.
- LangChain et LangChain OpenAI/Community.
- Mem0 via PostgreSQL/pgvector.
- `python-telegram-bot` pour Telegram.
- Intégrations HTTP via `httpx`.

### Données et services

- Supabase : PostgreSQL et pgvector.
- Migrations SQL dans `backend/migrations/`.
- RLS activée selon la documentation sécurité du projet.
- ElevenLabs et Whisper : [À REMPLIR]

## Structure principale

- `backend/main.py` : création de l'application FastAPI, CORS et enregistrement des routeurs.
- `backend/config.py` : paramètres issus de l'environnement.
- `backend/routers/` : endpoints chat, mémoire, emplois, voix et agents.
- `backend/agent/` : agent et outils métier.
- `backend/memory/` : client Mem0 et schémas mémoire.
- `backend/services/` : services d'authentification, Supabase et ElevenLabs.
- `backend/telegram_bot/` : bot et handlers Telegram.
- `backend/migrations/` : migrations de schéma, Mem0, RLS et fonctions.
- `frontend/app/` : routes et pages Next.js.
- `frontend/components/` : composants d'interface.
- `frontend/lib/` : client API, client Supabase et utilitaires.
- `docs/` : documentation générale du projet.

## Flux de données

1. L'utilisateur interagit avec le frontend Next.js ou le bot Telegram.
2. La requête est traitée par FastAPI ou les handlers Telegram.
3. Les routeurs délèguent aux services, à l'agent ou à la mémoire selon le cas.
4. Les données persistantes sont stockées dans Supabase/PostgreSQL, avec pgvector pour la recherche sémantique.

## Configuration et lancement

- Variables backend : `backend/.env`, à partir de `.env.example`.
- Variables frontend : `frontend/.env.local`, à partir de `frontend/.env.local.example`.
- Backend : `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` depuis `backend/`.
- Frontend : `npm run dev` depuis `frontend/`.
- Bot : `python telegram_bot/bot.py` depuis `backend/`.

## Dépendances et contraintes

- Vérifier `backend/requirements.txt` et `frontend/package.json` avant d'ajouter une dépendance.
- Les secrets ne doivent pas être commités.
- Toute modification de schéma doit suivre le système de migrations existant.