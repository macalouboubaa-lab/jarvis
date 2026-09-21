# Règles de codage

## Principes

- Préserver le périmètre souverain du projet et la propriété des données.
- Préférer les patterns et helpers déjà présents dans le dépôt.
- Ne pas introduire de dépendance sans vérifier les fichiers de dépendances et l'architecture.
- Ne pas exposer de secret, clé API ou valeur sensible dans le code, les logs ou la documentation.
- Ne pas modifier une migration déjà appliquée sans décision explicite ; créer une nouvelle migration si nécessaire.

## Backend Python

- Conserver les responsabilités séparées entre routeurs, services, agent, mémoire et bot Telegram.
- Utiliser les modèles et validations Pydantic existants lorsque le périmètre le permet.
- Respecter la configuration centralisée dans `backend/config.py`.
- Nommage et formatage : [À REMPLIR - outil et configuration de formatage/lint]

## Frontend TypeScript

- Conserver la séparation entre pages Next.js, composants et utilitaires de `frontend/lib/`.
- Réutiliser les composants et dépendances déjà installés avant d'en créer de nouveaux.
- Respecter les conventions TypeScript/React du code voisin.
- Formatage et lint : [À REMPLIR - configuration Prettier/ESLint]

## Documentation et commits

- Écrire la documentation en français, sauf nécessité technique.
- Mettre à jour `tasks.md` et `memory.md` après une session importante.
- Convention de commit : [À REMPLIR]
- Les tests et vérifications attendus avant commit : [À REMPLIR]

## Interdictions

- Ne pas écraser un fichier de contexte existant sans décision explicite.
- Ne pas ajouter de données fictives présentées comme des faits.
- Ne pas contourner l'authentification, la RLS ou les restrictions Telegram.
- Ne pas stocker les secrets dans Git.