-- 007_rls_policies.sql
-- Politiques RLS d'isolation par utilisateur authentifié.

ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_facts ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS chat_history_user_isolation ON chat_history;
CREATE POLICY chat_history_user_isolation
ON chat_history
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS knowledge_base_user_isolation ON knowledge_base;
CREATE POLICY knowledge_base_user_isolation
ON knowledge_base
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS user_facts_user_isolation ON user_facts;
CREATE POLICY user_facts_user_isolation
ON user_facts
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS job_applications_user_isolation ON job_applications;
CREATE POLICY job_applications_user_isolation
ON job_applications
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS courses_user_isolation ON courses;
CREATE POLICY courses_user_isolation
ON courses
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS opportunities_user_isolation ON opportunities;
CREATE POLICY opportunities_user_isolation
ON opportunities
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'memories'
          AND column_name = 'user_id'
    ) THEN
        EXECUTE 'ALTER TABLE memories ENABLE ROW LEVEL SECURITY';
        EXECUTE 'DROP POLICY IF EXISTS memories_user_isolation ON memories';
        EXECUTE '
            CREATE POLICY memories_user_isolation
            ON memories
            USING (auth.uid() = user_id)
            WITH CHECK (auth.uid() = user_id)
        ';
    END IF;
END
$$;
