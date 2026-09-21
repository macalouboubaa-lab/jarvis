# PRD - Jarvis

## Vision

Jarvis est un assistant IA personnel souverain. Les données, conversations, souvenirs et opportunités professionnelles doivent rester stockés dans l'infrastructure Supabase du propriétaire.

## Public cible

- [À REMPLIR]

## Cas d'usage

- Converser avec l'assistant depuis une interface Web.
- Utiliser l'assistant depuis Telegram avec des messages texte et des notes vocales.
- Conserver et retrouver des souvenirs via une mémoire sémantique.
- Rechercher et suivre des opportunités professionnelles.
- Suivre des cours.
- Utiliser la synthèse vocale et la transcription vocale.

## Exigences fonctionnelles

- Fournir une interface de chat Web.
- Exposer une API FastAPI pour le frontend et les intégrations.
- Proposer un agent outillé basé sur LangChain/LangGraph.
- Stocker la mémoire dans PostgreSQL avec pgvector via Supabase et Mem0.
- Restreindre l'accès du bot Telegram à `TELEGRAM_ALLOWED_USER_ID`.
- Conserver les données sur l'instance Supabase propriétaire.

## MVP actuel

- Squelette FastAPI et Next.js.
- Intégration Mem0 avec pgvector.
- Bot Telegram.
- Interface de chat Web avec audio et microphone.
- Intégrations prévues ou présentes pour ElevenLabs et Whisper.

## V2 / À planifier

- Connecteur n8n pour le scraping des offres d'emploi.
- Streaming vocal en temps réel ElevenLabs WebRTC.
- [À REMPLIR]

## Critères d'acceptation

- [À REMPLIR]