/*
  # Extensive Lessons and Quizzes
  Adds comprehensive lessons across all modules with 3 questions per lesson.
  Safe inserts via NOT EXISTS checks to avoid duplicates by (module_id, title).
*/

-- =====================
-- Module 1: Conceptos Básicos
-- =====================
-- Cambios de Estado y Energía
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 1 AND title = 'Cambios de Estado y Energía'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 1, 'Cambios de Estado y Energía',
       '<h2>Cambios de Estado</h2><p>Fusión, solidificación, vaporización, condensación, sublimación y deposición implican transferencias de energía (calor latente).</p>',
       7, 18 FROM ins;

-- Quizzes (3)
INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El paso de sólido a gas sin pasar por líquido se llama...',
       'multiple_choice',
       '["Sublimación", "Fusión", "Vaporización", "Condensación"]'::jsonb,
       'Sublimación',
       'La sublimación es el cambio directo de sólido a gas.',
       10, 1
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Cambios de Estado y Energía';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El calor latente de fusión se asocia con...',
       'multiple_choice',
       '["Cambio de estado", "Aumento de temperatura", "Disolución", "Neutralización"]'::jsonb,
       'Cambio de estado',
       'El calor latente se absorbe/libera durante el cambio de estado sin variar la temperatura.',
       10, 2
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Cambios de Estado y Energía';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: al hervir, la temperatura del líquido sigue aumentando.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'Durante la ebullición, la temperatura se mantiene constante mientras ocurre el cambio de estado.',
       10, 3
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Cambios de Estado y Energía';

-- Propiedades Intensivas vs Extensivas
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 1 AND title = 'Propiedades Intensivas vs Extensivas'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 1, 'Propiedades Intensivas vs Extensivas',
       '<h2>Clasificación de Propiedades</h2><p>Intensivas: independientes de la cantidad (densidad, color). Extensivas: dependen de la cantidad (masa, volumen).</p>',
       8, 16 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       '¿Cuál es una propiedad intensiva?',
       'multiple_choice',
       '["Densidad", "Masa", "Volumen", "Longitud"]'::jsonb,
       'Densidad',
       'La densidad no depende de la cantidad de sustancia.',
       10, 1
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Propiedades Intensivas vs Extensivas';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La masa es una propiedad...',
       'multiple_choice',
       '["Extensiva", "Intensiva", "Química", "Intrínseca"]'::jsonb,
       'Extensiva',
       'Las extensivas dependen de la cantidad, como la masa.',
       10, 2
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Propiedades Intensivas vs Extensivas';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: el color es intensivo.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Verdadero',
       'El color no depende de la cantidad de sustancia.',
       10, 3
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Propiedades Intensivas vs Extensivas';

-- Métodos de Separación de Mezclas
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 1 AND title = 'Métodos de Separación de Mezclas'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 1, 'Métodos de Separación de Mezclas',
       '<h2>Separación</h2><p>Filtración, decantación, destilación, cromatografía para separar componentes de mezclas.</p>',
       9, 18 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Para separar sólidos de líquidos se usa comúnmente...',
       'multiple_choice',
       '["Filtración", "Destilación", "Cromatografía", "Electrólisis"]'::jsonb,
       'Filtración',
       'La filtración retiene sólidos y deja pasar el líquido.',
       10, 1
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Métodos de Separación de Mezclas';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La destilación separa mezclas según...',
       'multiple_choice',
       '["Punto de ebullición", "Color", "Densidad", "Solubilidad"]'::jsonb,
       'Punto de ebullición',
       'Se basa en diferentes temperaturas de ebullición de los componentes.',
       10, 2
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Métodos de Separación de Mezclas';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: la cromatografía separa por afinidad diferencial.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Verdadero',
       'La cromatografía separa por distinta interacción con fase móvil/estacionaria.',
       10, 3
FROM lessons l WHERE l.module_id = 1 AND l.title = 'Métodos de Separación de Mezclas';

-- =====================
-- Module 2: Enlaces y Compuestos
-- =====================
-- Polaridad y Electronegatividad
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 2 AND title = 'Polaridad y Electronegatividad'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 2, 'Polaridad y Electronegatividad',
       '<h2>Polaridad</h2><p>La diferencia de electronegatividad y geometría molecular determinan polaridad.</p>',
       6, 18 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Una molécula es polar cuando...',
       'multiple_choice',
       '["Tiene momento dipolar neto", "Es lineal", "Es simétrica", "No tiene enlaces"]'::jsonb,
       'Tiene momento dipolar neto',
       'Polaridad implica distribución desigual de carga y momento dipolar.',
       10, 1
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Polaridad y Electronegatividad';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La diferencia de electronegatividad alta favorece...',
       'multiple_choice',
       '["Enlace iónico", "Enlace covalente puro", "Enlace metálico", "Ninguno"]'::jsonb,
       'Enlace iónico',
       'Grandes diferencias tienden a transferencia de electrones (iónico).',
       10, 2
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Polaridad y Electronegatividad';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: CO₂ es polar.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'CO₂ es lineal y sus dipolos se cancelan; es apolar.',
       10, 3
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Polaridad y Electronegatividad';

-- Geometría Molecular (VSEPR)
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 2 AND title = 'Geometría Molecular (VSEPR)'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 2, 'Geometría Molecular (VSEPR)',
       '<h2>VSEPR</h2><p>Repulsión de pares electrónicos define geometría: lineal, trigonal plana, tetraédrica, etc.</p>',
       7, 20 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'CH₄ (metano) tiene geometría...',
       'multiple_choice',
       '["Tetraédrica", "Trigonal plana", "Lineal", "Angular"]'::jsonb,
       'Tetraédrica',
       'Cuatro pares enlazantes alrededor de C generan geometría tetraédrica.',
       10, 1
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Geometría Molecular (VSEPR)';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'H₂O es...',
       'multiple_choice',
       '["Angular", "Lineal", "Tetraédrica", "Trigonal bipiramidal"]'::jsonb,
       'Angular',
       'Dos pares enlazantes y dos no enlazantes en O producen geometría angular.',
       10, 2
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Geometría Molecular (VSEPR)';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: BF₃ es trigonal planar.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Verdadero',
       'BF₃ con tres enlaces y sin pares libres en B es trigonal planar.',
       10, 3
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Geometría Molecular (VSEPR)';

-- Interacciones Intermoleculares
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 2 AND title = 'Interacciones Intermoleculares'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 2, 'Interacciones Intermoleculares',
       '<h2>Fuerzas</h2><p>Puentes de hidrógeno, dipolo-dipolo y fuerzas de dispersión (London).</p>',
       8, 18 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El punto de ebullición elevado del agua se debe a...',
       'multiple_choice',
       '["Puentes de hidrógeno", "Enlace iónico", "Fuerzas metálicas", "Dipolo inducido"]'::jsonb,
       'Puentes de hidrógeno',
       'Interacciones fuertes entre moléculas de agua elevan el punto de ebullición.',
       10, 1
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Interacciones Intermoleculares';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Las fuerzas London son...',
       'multiple_choice',
       '["Dipolos instantáneos", "Puentes de H", "Enlaces covalentes", "Enlaces iónicos"]'::jsonb,
       'Dipolos instantáneos',
       'Surgen por fluctuaciones temporales en la distribución electrónica.',
       10, 2
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Interacciones Intermoleculares';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: el NH₃ presenta puentes de hidrógeno.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Verdadero',
       'El N con par libre y H enlazado permite puentes de H entre moléculas.',
       10, 3
FROM lessons l WHERE l.module_id = 2 AND l.title = 'Interacciones Intermoleculares';

-- =====================
-- Module 3: Reacciones Químicas
-- =====================
-- Ley de Velocidad y Orden de Reacción
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 3 AND title = 'Ley de Velocidad y Orden de Reacción'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 3, 'Ley de Velocidad y Orden de Reacción',
       '<h2>Cinética</h2><p>La ley de velocidad relaciona la velocidad con concentraciones. El orden se obtiene de datos experimentales.</p>',
       6, 24 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La ley de velocidad general es...',
       'multiple_choice',
       '["v = k[A]^m[B]^n", "v = kA + B", "v = A/B", "v = k[A+B]"]'::jsonb,
       'v = k[A]^m[B]^n',
       'Relaciona velocidad con concentraciones elevadas a órdenes m y n.',
       10, 1
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Ley de Velocidad y Orden de Reacción';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El orden total de la reacción es...',
       'multiple_choice',
       '["m + n", "m × n", "m/n", "n - m"]'::jsonb,
       'm + n',
       'Orden total es la suma de los órdenes parciales.',
       10, 2
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Ley de Velocidad y Orden de Reacción';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: el orden de reacción se deduce de la ecuación balanceada.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'El orden se obtiene de datos experimentales, no de la ecuación balanceada.',
       10, 3
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Ley de Velocidad y Orden de Reacción';

-- Rendimiento y Reactivo Limitante
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 3 AND title = 'Rendimiento y Reactivo Limitante'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 3, 'Rendimiento y Reactivo Limitante',
       '<h2>Estequiometría aplicada</h2><p>El reactivo limitante determina el máximo de producto; rendimiento = (real/teórico)×100.</p>',
       7, 22 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El reactivo que se consume primero es...',
       'multiple_choice',
       '["Limitante", "En exceso", "Catalizador", "Intermedio"]'::jsonb,
       'Limitante',
       'El limitante determina el máximo de producto formado.',
       10, 1
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Rendimiento y Reactivo Limitante';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Si el rendimiento teórico es 10 g y el real 8 g, el % es...',
       'multiple_choice',
       '["80%", "90%", "100%", "20%"]'::jsonb,
       '80%',
       'Rendimiento = (8/10)×100 = 80%.',
       10, 2
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Rendimiento y Reactivo Limitante';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: el reactivo en exceso limita la reacción.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'El reactivo limitante es el que se consume primero y limita la reacción.',
       10, 3
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Rendimiento y Reactivo Limitante';

-- Tipos de Reacciones Orgánicas Básicas
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 3 AND title = 'Tipos de Reacciones Orgánicas Básicas'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 3, 'Tipos de Reacciones Orgánicas Básicas',
       '<h2>Orgánica básica</h2><p>Adición, sustitución y eliminación en hidrocarburos y derivados sencillos.</p>',
       8, 24 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La adición ocurre típicamente en...',
       'multiple_choice',
       '["Alquenos", "Alcanos", "Alquinos", "Arenos"]'::jsonb,
       'Alquenos',
       'Dobles enlaces permiten adición de átomos o grupos.',
       10, 1
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Tipos de Reacciones Orgánicas Básicas';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La sustitución electrófila aromática es típica de...',
       'multiple_choice',
       '["Benceno", "Metano", "Eteno", "Etino"]'::jsonb,
       'Benceno',
       'Anillos aromáticos sufren sustitución electrófila.',
       10, 2
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Tipos de Reacciones Orgánicas Básicas';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: la eliminación produce una insaturación.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Verdadero',
       'Al eliminar, se forma un doble enlace en muchos casos.',
       10, 3
FROM lessons l WHERE l.module_id = 3 AND l.title = 'Tipos de Reacciones Orgánicas Básicas';

-- =====================
-- Module 4: Química Avanzada
-- =====================
-- Equilibrio Químico
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 4 AND title = 'Equilibrio Químico'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 4, 'Equilibrio Químico',
       '<h2>Equilibrio</h2><p>Estado dinámico donde velocidades directa e inversa se igualan; constante K depende de temperatura.</p>',
       7, 26 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'La constante de equilibrio K depende de...',
       'multiple_choice',
       '["Temperatura", "Presión", "Catalizador", "Superficie"]'::jsonb,
       'Temperatura',
       'K es función de T; catalizadores no cambian K, solo velocidad.',
       10, 1
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Equilibrio Químico';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El principio de Le Châtelier predice...',
       'multiple_choice',
       '["Cómo responde el equilibrio a perturbaciones", "El orden de reacción", "La energía de activación", "La polaridad"]'::jsonb,
       'Cómo responde el equilibrio a perturbaciones',
       'Indica dirección del cambio ante variaciones en concentración, presión o temperatura.',
       10, 2
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Equilibrio Químico';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: en equilibrio, no ocurren reacciones.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'Equilibrio es dinámico: las reacciones directa e inversa continúan a igual velocidad.',
       10, 3
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Equilibrio Químico';

-- Ácido-Base: pH y Neutralización
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 4 AND title = 'Ácido-Base: pH y Neutralización'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 4, 'Ácido-Base: pH y Neutralización',
       '<h2>pH</h2><p>pH = -log[H+]; neutralización ácido-base, cálculo de pH en soluciones fuertes y débiles.</p>',
       8, 28 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Una solución con [H+] = 1×10^-3 M tiene pH ≈',
       'multiple_choice',
       '["3", "11", "7", "1"]'::jsonb,
       '3',
       'pH = -log(1×10^-3) = 3.',
       10, 1
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Ácido-Base: pH y Neutralización';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Al mezclar ácido fuerte con base fuerte en proporciones equivalentes, el pH final tiende a...',
       'multiple_choice',
       '["7", "3", "11", "1"]'::jsonb,
       '7',
       'Neutralización produce solución aproximadamente neutra (si no hay efectos de concentración/temperatura importantes).',
       10, 2
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Ácido-Base: pH y Neutralización';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: el pH de 2 es básico.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'pH bajo (<7) indica acidez; básico es >7.',
       10, 3
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Ácido-Base: pH y Neutralización';

-- Solubilidad y Producto de Solubilidad (Ksp)
WITH ins AS (
  SELECT 1 WHERE NOT EXISTS (
    SELECT 1 FROM lessons WHERE module_id = 4 AND title = 'Solubilidad y Producto de Solubilidad (Ksp)'
  )
)
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT 4, 'Solubilidad y Producto de Solubilidad (Ksp)',
       '<h2>Ksp</h2><p>El producto de solubilidad describe el equilibrio de solutos poco solubles; precipitación según el ion producto.</p>',
       9, 26 FROM ins;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Si el ion producto supera Ksp, ocurre...',
       'multiple_choice',
       '["Precipitación", "Disolución", "Neutralización", "Sublimación"]'::jsonb,
       'Precipitación',
       'Ion producto > Ksp favorece la formación de sólido (precipitado).',
       10, 1
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Solubilidad y Producto de Solubilidad (Ksp)';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'El Ksp depende principalmente de...',
       'multiple_choice',
       '["Temperatura", "Presión", "Volumen", "Velocidad"]'::jsonb,
       'Temperatura',
       'El Ksp es una constante de equilibrio que varía con la temperatura.',
       10, 2
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Solubilidad y Producto de Solubilidad (Ksp)';

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT l.id,
       'Verdadero o falso: todos los compuestos iónicos son muy solubles.',
       'true_false',
       '["Verdadero", "Falso"]'::jsonb,
       'Falso',
       'La solubilidad varía; algunos compuestos tienen Ksp muy bajo y precipitan fácilmente.',
       10, 3
FROM lessons l WHERE l.module_id = 4 AND l.title = 'Solubilidad y Producto de Solubilidad (Ksp)';