-- Ensure gen_random_uuid() is available
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Set default for id to gen_random_uuid()
ALTER TABLE "public"."quizzes"
  ALTER COLUMN "id" SET DEFAULT gen_random_uuid();

-- Add foreign key for lesson_id referencing public.lessons(id) if not exists
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint c
    JOIN pg_class t ON t.oid = c.conrelid
    WHERE c.conname = 'quizzes_lesson_id_fkey'
      AND t.relname = 'quizzes'
  ) THEN
    ALTER TABLE "public"."quizzes"
      ADD CONSTRAINT "quizzes_lesson_id_fkey"
      FOREIGN KEY ("lesson_id") REFERENCES "public"."lessons"("id")
      ON DELETE CASCADE;
  END IF;
END $$;