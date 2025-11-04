/*
  # Extra Lessons and Quizzes
  This migration adds additional lessons across all modules with one sample quiz each.
  Safe inserts: each lesson only inserts if a lesson with same module_id + title doesn't exist.
*/

-- Module 1: Conceptos Básicos
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 1 AND title = 'Propiedades de la Materia'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 1, 'Propiedades de la Materia',
       '<h2>Propiedades de la Materia</h2><p>La materia posee propiedades físicas (masa, volumen, densidad) y químicas (reactividad).</p>',
       5, 12 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       '¿Cuál de las siguientes es una propiedad física?',
       'multiple_choice',
       '["Densidad", "Reactividad", "Acidez", "Basicidad"]'::jsonb,
       'Densidad',
       'La densidad es una propiedad física; la reactividad es química.',
       10, 1
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Propiedades de la Materia';

WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 1 AND title = 'Mezclas y Sustancias'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 1, 'Mezclas y Sustancias',
       '<h2>Mezclas y Sustancias</h2><p>Diferencia entre sustancias puras y mezclas. Mezclas homogéneas vs heterogéneas.</p>',
       6, 12 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Una disolución salina es...',
       'multiple_choice',
       '["Mezcla homogénea", "Mezcla heterogénea", "Sustancia pura", "Elemento"]'::jsonb,
       'Mezcla homogénea',
       'La sal se disuelve uniformemente en agua, formando una mezcla homogénea.',
       10, 1
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Mezclas y Sustancias';

-- Module 2: Enlaces y Compuestos
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 2 AND title = 'Nomenclatura Básica'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 2, 'Nomenclatura Básica',
       '<h2>Nomenclatura</h2><p>Reglas sencillas para nombrar compuestos iónicos y covalentes.</p>',
       4, 18 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       '¿Cómo se llama NaCl?',
       'multiple_choice',
       '["Cloruro de sodio", "Oxido de sodio", "Sulfato de sodio", "Nitrato de sodio"]'::jsonb,
       'Cloruro de sodio',
       'NaCl se denomina cloruro de sodio (compuesto iónico).',
       10, 1
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Nomenclatura Básica';

WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 2 AND title = 'Compuestos Iónicos vs Covalentes'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 2, 'Compuestos Iónicos vs Covalentes',
       '<h2>Comparación</h2><p>Iónicos: redes cristalinas y alta conductividad en disolución. Covalentes: moléculas discretas.</p>',
       5, 16 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Los compuestos covalentes suelen...',
       'multiple_choice',
       '["Formar moléculas", "Formar redes cristalinas", "Conducir bien la electricidad en agua", "Tener puntos de fusión muy altos"]'::jsonb,
       'Formar moléculas',
       'Los compuestos covalentes forman moléculas discretas; los iónicos redes.',
       10, 1
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Compuestos Iónicos vs Covalentes';

-- Module 3: Reacciones Químicas
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 3 AND title = 'Energía de Activación'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 3, 'Energía de Activación',
       '<h2>Umbral energético</h2><p>La energía mínima necesaria para que ocurra una reacción.</p>',
       4, 20 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Un catalizador...',
       'multiple_choice',
       '["Disminuye la energía de activación", "Aumenta la energía de activación", "Detiene la reacción", "No afecta a la reacción"]'::jsonb,
       'Disminuye la energía de activación',
       'Los catalizadores reducen la energía de activación y aceleran la reacción.',
       10, 1
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Energía de Activación';

WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 3 AND title = 'Velocidad de Reacción'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 3, 'Velocidad de Reacción',
       '<h2>Cinética Química</h2><p>Factores que influyen: concentración, temperatura, superficie y catalizadores.</p>',
       5, 22 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Incrementar la temperatura generalmente...',
       'multiple_choice',
       '["Aumenta la velocidad", "Disminuye la velocidad", "No cambia la velocidad", "Detiene la reacción"]'::jsonb,
       'Aumenta la velocidad',
       'Mayor temperatura implica más colisiones eficaces, aumentando la velocidad.',
       10, 1
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Velocidad de Reacción';

-- Module 4: Química Avanzada
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 4 AND title = 'Ácidos y Bases: Fuertes y Débiles'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 4, 'Ácidos y Bases: Fuertes y Débiles',
       '<h2>Fuerza de ácidos y bases</h2><p>Grado de disociación en agua y relación con pKa/pKb.</p>',
       5, 24 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Un ácido fuerte en agua...',
       'multiple_choice',
       '["Se disocia casi completamente", "Se disocia muy poco", "No se disocia", "No afecta el pH"]'::jsonb,
       'Se disocia casi completamente',
       'Ácidos fuertes se disocian casi por completo, reduciendo el pH.',
       10, 1
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Ácidos y Bases: Fuertes y Débiles';

WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 4 AND title = 'Isomería Básica'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 4, 'Isomería Básica',
       '<h2>Isómeros</h2><p>Compuestos con misma fórmula molecular pero distinta estructura: estructurales y geométricos.</p>',
       6, 26 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Dos compuestos con la misma fórmula molecular pero distinta estructura son...',
       'multiple_choice',
       '["Isómeros", "Polímeros", "Electrolitos", "Coloides"]'::jsonb,
       'Isómeros',
       'La isomería describe compuestos con igual fórmula pero distinta disposición.',
       10, 1
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Isomería Básica';