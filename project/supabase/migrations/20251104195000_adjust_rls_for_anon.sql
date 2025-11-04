/*
  # Adjust RLS Policies for Anonymous Role (Desktop App)

  This migration relaxes read/write policies for content and user tables
  to work with the Supabase anon key (no JWT) in a desktop environment.

  NOTE: Suitable for local/educational desktop apps. For internet-facing
  deployments, consider using Supabase Auth and stricter RLS.
*/

-- Ensure required extension for gen_random_uuid
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Modules: allow anon SELECT
DO $$ BEGIN
  CREATE POLICY "Anon can view modules"
    ON modules FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Lessons: allow anon SELECT
DO $$ BEGIN
  CREATE POLICY "Anon can view lessons"
    ON lessons FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Quizzes: allow anon SELECT
DO $$ BEGIN
  CREATE POLICY "Anon can view quizzes"
    ON quizzes FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Achievements: allow anon SELECT
DO $$ BEGIN
  CREATE POLICY "Anon can view achievements"
    ON achievements FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- App Users: allow anon SELECT/INSERT/UPDATE (needed for local login/register)
DO $$ BEGIN
  CREATE POLICY "Anon can select app_users"
    ON app_users FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE POLICY "Anon can insert app_users"
    ON app_users FOR INSERT
    TO anon
    WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE POLICY "Anon can update app_users"
    ON app_users FOR UPDATE
    TO anon
    USING (true)
    WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- User Progress: allow anon SELECT/INSERT/UPDATE
DO $$ BEGIN
  CREATE POLICY "Anon can select user_progress"
    ON user_progress FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE POLICY "Anon can insert user_progress"
    ON user_progress FOR INSERT
    TO anon
    WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE POLICY "Anon can update user_progress"
    ON user_progress FOR UPDATE
    TO anon
    USING (true)
    WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- User Achievements: allow anon SELECT/INSERT
DO $$ BEGIN
  CREATE POLICY "Anon can select user_achievements"
    ON user_achievements FOR SELECT
    TO anon
    USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE POLICY "Anon can insert user_achievements"
    ON user_achievements FOR INSERT
    TO anon
    WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;