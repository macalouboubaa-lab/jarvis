# 🤖 Jarvis - Assistant IA Personnel Souverain

Jarvis est un assistant full-stack souverain conçu pour garantir que l'intégralité de vos données, conversations, souvenirs et opportunités professionnelles restent stockés dans **votre propre infrastructure Supabase** (PostgreSQL + pgvector).

## 🌟 Fonctionnalités

- **Interface de Chat Web** : Next.js 14, TailwindCSS (thème Iron Man sombre / cyan néon), audio et microphone.
- **Accès Mobile Telegram** : Bot interactif prenant en charge les commandes texte et les notes vocales.
- **Mémoire Sémantique Autohébergée** : Intégration Mem0 branchée directement sur PostgreSQL avec pgvector.
- **Agent Autonome** : LangChain / LangGraph outillé (recherche de candidatures, suivi de cours, mémorisation active).
- **Synthèse Vocale & STT** : Intégration ElevenLabs & Whisper.

## 🚀 Démarrage Rapide (Codespaces ou Local)

### 1. Variables d'environnement
```bash
cp .env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

### 2. Base de données Supabase
Exécutez le script situé dans `backend/migrations/001_init.sql` dans l'éditeur SQL de votre console Supabase.

### 3. Lancer le Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Lancer le Bot Telegram
```bash
cd backend
python telegram_bot/bot.py
```

### 5. Lancer le Frontend
```bash
cd frontend
npm install
npm run dev
```
Rendez-vous sur [http://localhost:3000/chat](http://localhost:3000/chat).
