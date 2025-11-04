/*
  # Module Introductions
  Adds an introductory lesson for each module if not present.
  Safe inserts via NOT EXISTS checks to avoid duplicates by (module_id, title).
*/

-- Module 1: Conceptos Básicos
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 1 AND title = 'Introducción a los Conceptos Básicos'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 1, 'Introducción a los Conceptos Básicos',
       '<h2>Bienvenido a Conceptos Básicos</h2><p>Exploraremos qué es la materia, sus estados y cómo se clasifica.</p>',
       1, 8 FROM ins;

-- Module 2: Enlaces y Compuestos
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 2 AND title = 'Introducción a Enlaces y Compuestos'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 2, 'Introducción a Enlaces y Compuestos',
       '<h2>Enlaces y Compuestos</h2><p>Aprenderás cómo se unen los átomos y cómo se forman distintas sustancias.</p>',
       1, 10 FROM ins;

-- Module 3: Reacciones Químicas
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 3 AND title = 'Introducción a las Reacciones Químicas'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 3, 'Introducción a las Reacciones Químicas',
       '<h2>¿Qué es una reacción?</h2><p>Conocerás cómo ocurren las reacciones y qué factores las afectan.</p>',
       1, 12 FROM ins;

-- Module 4: Química Avanzada
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 4 AND title = 'Introducción a Química Avanzada'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 4, 'Introducción a Química Avanzada',
       '<h2>Avanzando en Química</h2><p>Veremos conceptos como equilibrio químico, ácidos y bases e isomería.</p>',
       1, 14 FROM ins;