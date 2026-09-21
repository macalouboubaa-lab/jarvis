-- 005_opportunities_user_id.sql
-- Ajout de user_id sur opportunities pour l'isolation par utilisateur.
-- Étape 1/2 : colonne nullable pour ne pas casser les lignes existantes.
-- Étape 2/2 (migration 007 ultérieure) : backfill puis NOT NULL.

ALTER TABLE opportunities
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS idx_opportunities_user_id
ON opportunities(user_id);
