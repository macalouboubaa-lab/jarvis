-- 006_opportunities_backfill.sql
-- Attribution des opportunités historiques avant passage en NOT NULL.
-- Les lignes sans propriétaire sont attribuées au premier utilisateur Supabase
-- créé. Cette règle de secours doit être vérifiée avant exécution en production.

DO $$
DECLARE
    fallback_user_id UUID;
BEGIN
    SELECT id
    INTO fallback_user_id
    FROM auth.users
    ORDER BY created_at, id
    LIMIT 1;

    IF EXISTS (
        SELECT 1
        FROM opportunities
        WHERE user_id IS NULL
    ) AND fallback_user_id IS NULL THEN
        RAISE EXCEPTION
            'Cannot backfill opportunities.user_id: auth.users is empty';
    END IF;

    UPDATE opportunities
    SET user_id = fallback_user_id
    WHERE user_id IS NULL;
END
$$;

ALTER TABLE opportunities
ALTER COLUMN user_id SET NOT NULL;
