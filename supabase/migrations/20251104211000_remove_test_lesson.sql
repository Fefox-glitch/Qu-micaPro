-- Elimina la lección de prueba y sus dependencias (quizzes y progreso)
-- Ejecutar en Supabase Postgres
BEGIN;

WITH test_lessons AS (
  SELECT id
  FROM public.lessons
  WHERE title ILIKE '%lección de prueba%'
     OR title ILIKE '%leccion de prueba%'
)
DELETE FROM public.quizzes q
USING test_lessons tl
WHERE q.lesson_id = tl.id;

DELETE FROM public.user_progress up
USING test_lessons tl
WHERE up.lesson_id = tl.id;

DELETE FROM public.lessons l
USING test_lessons tl
WHERE l.id = tl.id;

COMMIT;