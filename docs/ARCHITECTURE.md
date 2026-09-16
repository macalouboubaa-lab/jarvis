# Architecture Système de Jarvis

```
Utilisateur (Web Next.js / Mobile Telegram)
                   │
                   ▼
             FastAPI Core
        ┌──────────┴──────────┐
        ▼                     ▼
 LangChain Agent        Mem0 Memory
        │                     │
        ▼                     ▼
Supabase Database (PostgreSQL + pgvector)
```
