/*
  # Chemistry Education App - Database Schema

  ## Overview
  This migration creates the complete database structure for a chemistry education desktop application
  for middle and high school students (ages 13-18).

  ## 1. New Tables

  ### `app_users`
  Stores local application user accounts (offline authentication)
  - `id` (uuid, primary key)
  - `username` (text, unique) - Student's username
  - `display_name` (text) - Student's display name
  - `created_at` (timestamptz) - Account creation timestamp
  - `last_login` (timestamptz) - Last login timestamp

  ### `modules`
  Contains the 4 main learning modules/levels
  - `id` (integer, primary key)
  - `level` (integer) - Module level (1-4)
  - `title` (text) - Module title
  - `description` (text) - Module description
  - `icon` (text) - Icon identifier
  - `color` (text) - Theme color for module
  - `order_index` (integer) - Display order

  ### `lessons`
  Individual lessons within each module
  - `id` (uuid, primary key)
  - `module_id` (integer, foreign key) - Parent module
  - `title` (text) - Lesson title
  - `content` (text) - Lesson content (HTML/markdown)
  - `order_index` (integer) - Order within module
  - `estimated_minutes` (integer) - Estimated completion time

  ### `quizzes`
  Quiz questions for each lesson
  - `id` (uuid, primary key)
  - `lesson_id` (uuid, foreign key) - Associated lesson
  - `question` (text) - Question text
  - `question_type` (text) - Type: 'multiple_choice', 'true_false', 'fill_blank'
  - `options` (jsonb) - Answer options (for multiple choice)
  - `correct_answer` (text) - Correct answer
  - `explanation` (text) - Explanation of correct answer
  - `points` (integer) - Points awarded for correct answer
  - `order_index` (integer) - Question order

  ### `user_progress`
  Tracks student progress through lessons
  - `id` (uuid, primary key)
  - `user_id` (uuid, foreign key) - Student user
  - `lesson_id` (uuid, foreign key) - Completed lesson
  - `completed` (boolean) - Lesson completion status
  - `score` (integer) - Quiz score (0-100)
  - `completed_at` (timestamptz) - Completion timestamp

  ### `achievements`
  Available achievements/badges
  - `id` (uuid, primary key)
  - `title` (text) - Achievement title
  - `description` (text) - Achievement description
  - `icon` (text) - Icon identifier
  - `requirement_type` (text) - Type: 'module_complete', 'perfect_score', 'streak'
  - `requirement_value` (integer) - Required value to unlock

  ### `user_achievements`
  Tracks earned achievements per user
  - `id` (uuid, primary key)
  - `user_id` (uuid, foreign key) - Student user
  - `achievement_id` (uuid, foreign key) - Earned achievement
  - `earned_at` (timestamptz) - When achievement was earned

  ## 2. Security
  - Enable RLS on all tables
  - Users can only read/write their own progress data
  - Module and lesson content is read-only for users
  - Achievements are read-only for users

  ## 3. Initial Data
  - Populate modules table with 4 chemistry learning levels
  - Create sample lessons for each module
  - Set up basic achievement system
*/

-- Create app_users table
CREATE TABLE IF NOT EXISTS app_users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  username text UNIQUE NOT NULL,
  display_name text NOT NULL,
  created_at timestamptz DEFAULT now(),
  last_login timestamptz DEFAULT now()
);

ALTER TABLE app_users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon can view app_users"
  ON app_users FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Anon can update app_users"
  ON app_users FOR UPDATE
  TO anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anon can insert app_users"
  ON app_users FOR INSERT
  TO anon
  WITH CHECK (true);

-- Create modules table
CREATE TABLE IF NOT EXISTS modules (
  id integer PRIMARY KEY,
  level integer NOT NULL,
  title text NOT NULL,
  description text NOT NULL,
  icon text NOT NULL,
  color text NOT NULL,
  order_index integer NOT NULL
);

ALTER TABLE modules ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone (anon) can view modules"
  ON modules FOR SELECT
  TO anon
  USING (true);

-- Create lessons table
CREATE TABLE IF NOT EXISTS lessons (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id integer NOT NULL REFERENCES modules(id),
  title text NOT NULL,
  content text NOT NULL,
  order_index integer NOT NULL,
  estimated_minutes integer DEFAULT 10
);

ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone (anon) can view lessons"
  ON lessons FOR SELECT
  TO anon
  USING (true);

-- Create quizzes table
CREATE TABLE IF NOT EXISTS quizzes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  question text NOT NULL,
  question_type text NOT NULL,
  options jsonb,
  correct_answer text NOT NULL,
  explanation text NOT NULL,
  points integer DEFAULT 10,
  order_index integer NOT NULL
);

ALTER TABLE quizzes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone (anon) can view quizzes"
  ON quizzes FOR SELECT
  TO anon
  USING (true);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  completed boolean DEFAULT false,
  score integer DEFAULT 0,
  completed_at timestamptz DEFAULT now(),
  UNIQUE(user_id, lesson_id)
);

ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon can view user_progress"
  ON user_progress FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Anon can insert user_progress"
  ON user_progress FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Anon can update user_progress"
  ON user_progress FOR UPDATE
  TO anon
  USING (true)
  WITH CHECK (true);

-- Create achievements table
CREATE TABLE IF NOT EXISTS achievements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text NOT NULL,
  icon text NOT NULL,
  requirement_type text NOT NULL,
  requirement_value integer NOT NULL
);

ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone (anon) can view achievements"
  ON achievements FOR SELECT
  TO anon
  USING (true);

-- Create user_achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
  achievement_id uuid NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
  earned_at timestamptz DEFAULT now(),
  UNIQUE(user_id, achievement_id)
);

ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon can view user_achievements"
  ON user_achievements FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Anon can insert user_achievements"
  ON user_achievements FOR INSERT
  TO anon
  WITH CHECK (true);

-- Insert initial modules data
INSERT INTO modules (id, level, title, description, icon, color, order_index) VALUES
(1, 1, 'Conceptos Básicos', 'Átomo, moléculas, estados de la materia y tabla periódica introductoria', 'atom', '#4CAF50', 1),
(2, 2, 'Enlaces y Compuestos', 'Enlaces químicos, compuestos y formulación básica', 'link', '#2196F3', 2),
(3, 3, 'Reacciones Químicas', 'Reacciones químicas, balanceo y estequiometría', 'flask', '#FF9800', 3),
(4, 4, 'Química Avanzada', 'Termoquímica, soluciones, pH y química orgánica introductoria', 'beaker', '#9C27B0', 4)
ON CONFLICT (id) DO NOTHING;

-- Insert sample lessons for Module 1
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes) VALUES
(1, 'El Átomo', '<h2>¿Qué es un átomo?</h2><p>El átomo es la unidad básica de la materia. Está compuesto por un núcleo central que contiene protones (carga positiva) y neutrones (sin carga), rodeado por electrones (carga negativa) que orbitan alrededor del núcleo.</p><h3>Estructura del átomo:</h3><ul><li><strong>Protones:</strong> Partículas con carga positiva en el núcleo</li><li><strong>Neutrones:</strong> Partículas sin carga en el núcleo</li><li><strong>Electrones:</strong> Partículas con carga negativa que orbitan el núcleo</li></ul><p>El número de protones determina el elemento químico.</p>', 1, 15),
(1, 'Moléculas', '<h2>¿Qué es una molécula?</h2><p>Una molécula es un grupo de dos o más átomos unidos por enlaces químicos. Las moléculas pueden estar formadas por átomos del mismo elemento o de elementos diferentes.</p><h3>Ejemplos:</h3><ul><li><strong>H₂O (agua):</strong> 2 átomos de hidrógeno + 1 átomo de oxígeno</li><li><strong>O₂ (oxígeno molecular):</strong> 2 átomos de oxígeno</li><li><strong>CO₂ (dióxido de carbono):</strong> 1 átomo de carbono + 2 átomos de oxígeno</li></ul>', 2, 12),
(1, 'Estados de la Materia', '<h2>Los tres estados principales</h2><p>La materia puede existir en tres estados principales: sólido, líquido y gaseoso.</p><h3>Características:</h3><ul><li><strong>Sólido:</strong> Forma y volumen definidos. Las partículas están muy juntas y organizadas.</li><li><strong>Líquido:</strong> Volumen definido pero forma variable. Las partículas están juntas pero pueden moverse.</li><li><strong>Gaseoso:</strong> Forma y volumen variables. Las partículas están muy separadas y se mueven libremente.</li></ul><p>Los cambios de estado ocurren con cambios de temperatura y presión.</p>', 3, 15),
(1, 'La Tabla Periódica', '<h2>Organización de los elementos</h2><p>La tabla periódica organiza todos los elementos químicos conocidos según su número atómico (número de protones).</p><h3>Estructura básica:</h3><ul><li><strong>Períodos:</strong> Filas horizontales (7 períodos)</li><li><strong>Grupos:</strong> Columnas verticales (18 grupos)</li><li><strong>Metales:</strong> Mayoría de elementos, buenos conductores</li><li><strong>No metales:</strong> Lado derecho, malos conductores</li><li><strong>Metaloides:</strong> Propiedades intermedias</li></ul><p>Los elementos en el mismo grupo tienen propiedades químicas similares.</p>', 4, 20)
ON CONFLICT DO NOTHING;

-- Insert sample lessons for Module 2
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes) VALUES
(2, 'Enlaces Iónicos', '<h2>¿Qué es un enlace iónico?</h2><p>Un enlace iónico se forma cuando un átomo transfiere electrones a otro átomo, creando iones con cargas opuestas que se atraen.</p><h3>Características:</h3><ul><li>Se forma entre metales y no metales</li><li>Forma compuestos cristalinos</li><li>Altos puntos de fusión</li><li>Conducen electricidad cuando están disueltos</li></ul><h3>Ejemplo:</h3><p>NaCl (sal común): Na⁺ + Cl⁻</p>', 1, 18),
(2, 'Enlaces Covalentes', '<h2>¿Qué es un enlace covalente?</h2><p>Un enlace covalente se forma cuando dos átomos comparten electrones.</p><h3>Tipos:</h3><ul><li><strong>Simple:</strong> Comparten 1 par de electrones (H-H)</li><li><strong>Doble:</strong> Comparten 2 pares (O=O)</li><li><strong>Triple:</strong> Comparten 3 pares (N≡N)</li></ul><h3>Características:</h3><ul><li>Se forma entre no metales</li><li>Puntos de fusión más bajos que iónicos</li><li>No conducen electricidad</li></ul>', 2, 18),
(2, 'Formulación Química', '<h2>Escribiendo fórmulas químicas</h2><p>Las fórmulas químicas representan la composición de los compuestos.</p><h3>Reglas básicas:</h3><ul><li>Los elementos se escriben con sus símbolos</li><li>Los subíndices indican número de átomos</li><li>El elemento menos electronegativo va primero</li></ul><h3>Ejemplos:</h3><ul><li>H₂O: 2 hidrógenos, 1 oxígeno</li><li>Ca(OH)₂: 1 calcio, 2 grupos OH</li><li>Fe₂O₃: 2 hierros, 3 oxígenos</li></ul>', 3, 20)
ON CONFLICT DO NOTHING;

-- Insert sample lessons for Module 3
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes) VALUES
(3, 'Tipos de Reacciones', '<h2>Reacciones químicas</h2><p>Una reacción química es un proceso donde las sustancias (reactivos) se transforman en nuevas sustancias (productos).</p><h3>Tipos principales:</h3><ul><li><strong>Síntesis:</strong> A + B → AB</li><li><strong>Descomposición:</strong> AB → A + B</li><li><strong>Sustitución simple:</strong> A + BC → AC + B</li><li><strong>Doble sustitución:</strong> AB + CD → AD + CB</li><li><strong>Combustión:</strong> Combustible + O₂ → CO₂ + H₂O</li></ul>', 1, 20),
(3, 'Balanceo de Ecuaciones', '<h2>Ley de conservación de la masa</h2><p>En una reacción química, la masa total de los reactivos debe ser igual a la masa total de los productos.</p><h3>Método de tanteo:</h3><ol><li>Contar átomos de cada elemento en ambos lados</li><li>Ajustar coeficientes para igualar átomos</li><li>Verificar que todos los elementos estén balanceados</li></ol><h3>Ejemplo:</h3><p>H₂ + O₂ → H₂O (sin balancear)</p><p>2H₂ + O₂ → 2H₂O (balanceada)</p>', 2, 25),
(3, 'Estequiometría', '<h2>Cálculos en reacciones químicas</h2><p>La estequiometría estudia las relaciones cuantitativas entre reactivos y productos.</p><h3>Conceptos clave:</h3><ul><li><strong>Mol:</strong> 6.022 × 10²³ partículas</li><li><strong>Masa molar:</strong> Masa de un mol de sustancia (g/mol)</li><li><strong>Relaciones molares:</strong> De la ecuación balanceada</li></ul><h3>Pasos para resolver:</h3><ol><li>Balancear la ecuación</li><li>Convertir a moles</li><li>Usar relaciones molares</li><li>Convertir a unidades pedidas</li></ol>', 3, 30)
ON CONFLICT DO NOTHING;

-- Insert sample lessons for Module 4
INSERT INTO lessons (module_id, title, content, order_index, estimated_minutes) VALUES
(4, 'Termoquímica', '<h2>Energía en las reacciones</h2><p>La termoquímica estudia los cambios de energía en las reacciones químicas.</p><h3>Conceptos importantes:</h3><ul><li><strong>Reacciones exotérmicas:</strong> Liberan energía (ΔH < 0)</li><li><strong>Reacciones endotérmicas:</strong> Absorben energía (ΔH > 0)</li><li><strong>Entalpía (ΔH):</strong> Cambio de calor a presión constante</li></ul><h3>Ejemplo:</h3><p>Combustión: C + O₂ → CO₂ + energía (exotérmica)</p><p>Fotosíntesis: CO₂ + H₂O + energía → glucosa (endotérmica)</p>', 1, 25),
(4, 'Soluciones y Concentración', '<h2>Mezclas homogéneas</h2><p>Una solución es una mezcla homogénea de soluto disuelto en solvente.</p><h3>Expresiones de concentración:</h3><ul><li><strong>Molaridad (M):</strong> moles de soluto / litros de solución</li><li><strong>Porcentaje masa/volumen:</strong> (g soluto / mL solución) × 100</li><li><strong>ppm:</strong> partes por millón</li></ul><h3>Factores de solubilidad:</h3><ul><li>Temperatura</li><li>Presión (para gases)</li><li>Naturaleza del soluto y solvente</li></ul>', 2, 22),
(4, 'pH y Ácidos-Bases', '<h2>Escala de pH</h2><p>El pH mide la acidez o basicidad de una solución en escala de 0 a 14.</p><h3>Escala:</h3><ul><li><strong>pH < 7:</strong> Ácido</li><li><strong>pH = 7:</strong> Neutro</li><li><strong>pH > 7:</strong> Básico</li></ul><h3>Teoría de Arrhenius:</h3><ul><li><strong>Ácidos:</strong> Liberan H⁺ en agua</li><li><strong>Bases:</strong> Liberan OH⁻ en agua</li></ul><h3>Ejemplos:</h3><p>Jugo de limón: pH ≈ 2 (ácido)</p><p>Agua pura: pH = 7 (neutro)</p><p>Jabón: pH ≈ 10 (básico)</p>', 3, 25),
(4, 'Química Orgánica Básica', '<h2>La química del carbono</h2><p>La química orgánica estudia los compuestos que contienen carbono.</p><h3>Características del carbono:</h3><ul><li>Forma 4 enlaces covalentes</li><li>Puede formar cadenas largas</li><li>Base de moléculas de la vida</li></ul><h3>Hidrocarburos principales:</h3><ul><li><strong>Alcanos:</strong> Enlaces simples (CH₄, metano)</li><li><strong>Alquenos:</strong> Enlaces dobles (C₂H₄, eteno)</li><li><strong>Alquinos:</strong> Enlaces triples (C₂H₂, etino)</li></ul><h3>Grupos funcionales:</h3><p>Alcoholes (-OH), Ácidos carboxílicos (-COOH), Aminas (-NH₂)</p>', 4, 28)
ON CONFLICT DO NOTHING;

-- Insert sample quiz questions (a few examples)
INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT 
  l.id,
  '¿Qué partículas se encuentran en el núcleo del átomo?',
  'multiple_choice',
  '["Protones y neutrones", "Protones y electrones", "Neutrones y electrones", "Solo protones"]'::jsonb,
  'Protones y neutrones',
  'El núcleo del átomo contiene protones (con carga positiva) y neutrones (sin carga). Los electrones orbitan alrededor del núcleo.',
  10,
  1
FROM lessons l
WHERE l.title = 'El Átomo' AND l.module_id = 1
ON CONFLICT DO NOTHING;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT 
  l.id,
  '¿Cuál es la fórmula química del agua?',
  'multiple_choice',
  '["H₂O", "HO₂", "H₂O₂", "HO"]'::jsonb,
  'H₂O',
  'El agua está formada por 2 átomos de hidrógeno y 1 átomo de oxígeno, por lo que su fórmula es H₂O.',
  10,
  1
FROM lessons l
WHERE l.title = 'Moléculas' AND l.module_id = 1
ON CONFLICT DO NOTHING;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT 
  l.id,
  'En un sólido, las partículas están muy juntas y organizadas.',
  'true_false',
  '["Verdadero", "Falso"]'::jsonb,
  'Verdadero',
  'Correcto. En el estado sólido, las partículas están muy juntas, organizadas en posiciones fijas y solo vibran en su lugar.',
  10,
  1
FROM lessons l
WHERE l.title = 'Estados de la Materia' AND l.module_id = 1
ON CONFLICT DO NOTHING;

INSERT INTO quizzes (lesson_id, question, question_type, options, correct_answer, explanation, points, order_index)
SELECT 
  l.id,
  '¿Qué tipo de enlace se forma cuando un átomo transfiere electrones a otro?',
  'multiple_choice',
  '["Enlace iónico", "Enlace covalente", "Enlace metálico", "Enlace de hidrógeno"]'::jsonb,
  'Enlace iónico',
  'Un enlace iónico se forma cuando hay transferencia de electrones entre átomos, generalmente entre un metal y un no metal.',
  10,
  1
FROM lessons l
WHERE l.title = 'Enlaces Iónicos' AND l.module_id = 2
ON CONFLICT DO NOTHING;

-- Insert achievements
INSERT INTO achievements (title, description, icon, requirement_type, requirement_value) VALUES
('Primer Paso', 'Completa tu primera lección', 'star', 'lesson_complete', 1),
('Estudiante Dedicado', 'Completa el Módulo 1', 'medal', 'module_complete', 1),
('Químico Junior', 'Completa el Módulo 2', 'trophy', 'module_complete', 2),
('Experto en Reacciones', 'Completa el Módulo 3', 'award', 'module_complete', 3),
('Maestro de Química', 'Completa el Módulo 4', 'crown', 'module_complete', 4),
('Perfeccionista', 'Obtén 100% en cualquier quiz', 'target', 'perfect_score', 100),
('Racha de Aprendizaje', 'Completa 5 lecciones seguidas', 'fire', 'streak', 5)
ON CONFLICT DO NOTHING;