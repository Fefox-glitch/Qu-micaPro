/*
  # Introducciones por Módulo (idempotente)
  Agrega una lección de introducción para cada módulo con contenido HTML
  y actualiza lecciones existentes con contenido vacío o placeholder.

  Estrategia:
  - INSERT si no existe (module_id, title)
  - UPDATE si existe y el content está vacío o es 'Contenido próximamente.'
*/

-- =====================
-- Módulo 1: Conceptos Básicos
-- =====================
-- Insertar la lección de introducción si no existe
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT m.id,
       'Introducción a Conceptos Básicos',
       '<h2>Bienvenido al Módulo: Conceptos Básicos</h2>' ||
       '<p>En este módulo estudiarás los cimientos de la química: el átomo, las moléculas, los estados de la materia y la tabla periódica.</p>' ||
       '<h3>Lo que aprenderás</h3><ul>' ||
       '<li>Partes del átomo y cómo se organizan</li>' ||
       '<li>Qué es una molécula y ejemplos cotidianos</li>' ||
       '<li>Estados de la materia y sus cambios</li>' ||
       '<li>Cómo está organizada la tabla periódica</li>' ||
       '</ul>' ||
       '<p>Consejo: avanza en orden y completa los cuestionarios para reforzar conceptos.</p>',
       0, 10
FROM modules m
WHERE m.title = 'Conceptos Básicos'
AND NOT EXISTS (
  SELECT 1 FROM lessons l WHERE l.module_id = m.id AND l.title = 'Introducción a Conceptos Básicos'
);

-- Actualizar si existe con contenido vacío o placeholder
UPDATE lessons l
SET content = '<h2>Bienvenido al Módulo: Conceptos Básicos</h2>' ||
              '<p>En este módulo estudiarás los cimientos de la química: el átomo, las moléculas, los estados de la materia y la tabla periódica.</p>' ||
              '<h3>Lo que aprenderás</h3><ul>' ||
              '<li>Partes del átomo y cómo se organizan</li>' ||
              '<li>Qué es una molécula y ejemplos cotidianos</li>' ||
              '<li>Estados de la materia y sus cambios</li>' ||
              '<li>Cómo está organizada la tabla periódica</li>' ||
              '</ul>' ||
              '<p>Consejo: avanza en orden y completa los cuestionarios para reforzar conceptos.</p>',
    order_index = 0,
    estimated_minutes = COALESCE(estimated_minutes, 10)
FROM modules m
WHERE l.module_id = m.id
  AND m.title = 'Conceptos Básicos'
  AND l.title = 'Introducción a Conceptos Básicos'
  AND (l.content IS NULL OR l.content = '' OR l.content = 'Contenido próximamente.');

-- =====================
-- Módulo 2: Enlaces y Compuestos
-- =====================
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT m.id,
       'Introducción a Enlaces y Compuestos',
       '<h2>Bienvenido al Módulo: Enlaces y Compuestos</h2>' ||
       '<p>Aquí aprenderás cómo se unen los átomos para formar sustancias: enlaces iónicos y covalentes, reglas básicas de formulación y propiedades de los compuestos.</p>' ||
       '<h3>Temas clave</h3><ul>' ||
       '<li>Diferencias entre enlaces iónicos y covalentes</li>' ||
       '<li>Electronegatividad y polaridad molecular (visión general)</li>' ||
       '<li>Reglas de nomenclatura y formulación química</li>' ||
       '<li>Propiedades macroscópicas de los compuestos</li>' ||
       '</ul>' ||
       '<p>Consejo: compara ejemplos reales (sal, agua, dióxido de carbono) para entender mejor.</p>',
       0, 12
FROM modules m
WHERE m.title = 'Enlaces y Compuestos'
AND NOT EXISTS (
  SELECT 1 FROM lessons l WHERE l.module_id = m.id AND l.title = 'Introducción a Enlaces y Compuestos'
);

UPDATE lessons l
SET content = '<h2>Bienvenido al Módulo: Enlaces y Compuestos</h2>' ||
              '<p>Aquí aprenderás cómo se unen los átomos para formar sustancias: enlaces iónicos y covalentes, reglas básicas de formulación y propiedades de los compuestos.</p>' ||
              '<h3>Temas clave</h3><ul>' ||
              '<li>Diferencias entre enlaces iónicos y covalentes</li>' ||
              '<li>Electronegatividad y polaridad molecular (visión general)</li>' ||
              '<li>Reglas de nomenclatura y formulación química</li>' ||
              '<li>Propiedades macroscópicas de los compuestos</li>' ||
              '</ul>' ||
              '<p>Consejo: compara ejemplos reales (sal, agua, dióxido de carbono) para entender mejor.</p>',
    order_index = 0,
    estimated_minutes = COALESCE(estimated_minutes, 12)
FROM modules m
WHERE l.module_id = m.id
  AND m.title = 'Enlaces y Compuestos'
  AND l.title = 'Introducción a Enlaces y Compuestos'
  AND (l.content IS NULL OR l.content = '' OR l.content = 'Contenido próximamente.');

-- =====================
-- Módulo 3: Reacciones Químicas
-- =====================
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT m.id,
       'Introducción a Reacciones Químicas',
       '<h2>Bienvenido al Módulo: Reacciones Químicas</h2>' ||
       '<p>Descubrirás cómo y por qué ocurren las reacciones, cómo balancearlas y cómo calcular cantidades de productos y reactivos.</p>' ||
       '<h3>Enfoque del módulo</h3><ul>' ||
       '<li>Tipos comunes de reacción (síntesis, descomposición, sustitución, combustión)</li>' ||
       '<li>Balanceo de ecuaciones químicas</li>' ||
       '<li>Estequiometría y relaciones molares</li>' ||
       '</ul>' ||
       '<p>Consejo: practica problemas cortos después de cada tema para dominar los cálculos.</p>',
       0, 12
FROM modules m
WHERE m.title = 'Reacciones Químicas'
AND NOT EXISTS (
  SELECT 1 FROM lessons l WHERE l.module_id = m.id AND l.title = 'Introducción a Reacciones Químicas'
);

UPDATE lessons l
SET content = '<h2>Bienvenido al Módulo: Reacciones Químicas</h2>' ||
              '<p>Descubrirás cómo y por qué ocurren las reacciones, cómo balancearlas y cómo calcular cantidades de productos y reactivos.</p>' ||
              '<h3>Enfoque del módulo</h3><ul>' ||
              '<li>Tipos comunes de reacción (síntesis, descomposición, sustitución, combustión)</li>' ||
              '<li>Balanceo de ecuaciones químicas</li>' ||
              '<li>Estequiometría y relaciones molares</li>' ||
              '</ul>' ||
              '<p>Consejo: practica problemas cortos después de cada tema para dominar los cálculos.</p>',
    order_index = 0,
    estimated_minutes = COALESCE(estimated_minutes, 12)
FROM modules m
WHERE l.module_id = m.id
  AND m.title = 'Reacciones Químicas'
  AND l.title = 'Introducción a Reacciones Químicas'
  AND (l.content IS NULL OR l.content = '' OR l.content = 'Contenido próximamente.');

-- =====================
-- Módulo 4: Química Avanzada
-- =====================
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes)
SELECT m.id,
       'Introducción a Química Avanzada',
       '<h2>Bienvenido al Módulo: Química Avanzada</h2>' ||
       '<p>Profundizarás en conceptos como termoquímica, equilibrio, soluciones, pH y una introducción a química orgánica.</p>' ||
       '<h3>Qué abarcaremos</h3><ul>' ||
       '<li>Termoquímica y cambios de energía</li>' ||
       '<li>Soluciones, concentración y factores de solubilidad</li>' ||
       '<li>Ácidos, bases y la escala de pH</li>' ||
       '<li>Fundamentos de química orgánica</li>' ||
       '</ul>' ||
       '<p>Consejo: relaciona los conceptos con fenómenos cotidianos (temperatura, disoluciones, limpieza, alimentos).</p>',
       0, 14
FROM modules m
WHERE m.title = 'Química Avanzada'
AND NOT EXISTS (
  SELECT 1 FROM lessons l WHERE l.module_id = m.id AND l.title = 'Introducción a Química Avanzada'
);

UPDATE lessons l
SET content = '<h2>Bienvenido al Módulo: Química Avanzada</h2>' ||
              '<p>Profundizarás en conceptos como termoquímica, equilibrio, soluciones, pH y una introducción a química orgánica.</p>' ||
              '<h3>Qué abarcaremos</h3><ul>' ||
              '<li>Termoquímica y cambios de energía</li>' ||
              '<li>Soluciones, concentración y factores de solubilidad</li>' ||
              '<li>Ácidos, bases y la escala de pH</li>' ||
              '<li>Fundamentos de química orgánica</li>' ||
              '</ul>' ||
              '<p>Consejo: relaciona los conceptos con fenómenos cotidianos (temperatura, disoluciones, limpieza, alimentos).</p>',
    order_index = 0,
    estimated_minutes = COALESCE(estimated_minutes, 14)
FROM modules m
WHERE l.module_id = m.id
  AND m.title = 'Química Avanzada'
  AND l.title = 'Introducción a Química Avanzada'
  AND (l.content IS NULL OR l.content = '' OR l.content = 'Contenido próximamente.');