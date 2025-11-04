-- Inserta/actualiza quizzes para la lección 7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767
-- Usa ON CONFLICT para permitir re-ejecuciones sin fallar por duplicados

INSERT INTO "public"."quizzes" (
  "id","lesson_id","question","question_type","options","correct_answer","explanation","points","order_index"
) VALUES
 ('b6f4dcb8-67e5-42de-8f64-1a561fc93891','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué es un átomo?','multiple_choice','["La unidad básica de la materia","Una molécula","Una mezcla de sustancias","Un tipo de energía"]','La unidad básica de la materia','Un átomo es la unidad más pequeña de la materia que conserva propiedades químicas.',10,1),
 ('7a2cbd30-624f-43b9-95e7-51e576ffaf6c','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es la carga del electrón?','multiple_choice','["Positiva","Negativa","Neutra","Depende del átomo"]','Negativa','Los electrones tienen carga negativa; los protones positiva y los neutrones no tienen carga.',10,2),
 ('c92d298c-50cf-4218-bbda-7f4e4c078b45','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál de las siguientes es una molécula?','multiple_choice','["O₂","O","H","Ne"]','O₂','Una molécula es dos o más átomos unidos; O₂ son dos átomos de oxígeno.',10,3),
 ('9b7f8f63-2f36-4e0d-94cd-9f2c53a53f66','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','El agua es un ejemplo de:','multiple_choice','["Elemento","Compuesto","Mezcla","Energía"]','Compuesto','El agua (H₂O) es un compuesto formado por hidrógeno y oxígeno.',10,4),
 ('e0f57e2a-34b3-42a6-a5f5-dfb24fa72c94','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué significa “estado sólido”?','multiple_choice','["Forma y volumen fijos","Volumen fijo pero forma variable","No tiene forma ni volumen","Estado de energía"]','Forma y volumen fijos','En el estado sólido las partículas están muy juntas y mantienen forma y volumen fijo.',10,5)
ON CONFLICT (id) DO UPDATE SET
  lesson_id = EXCLUDED.lesson_id,
  question = EXCLUDED.question,
  question_type = EXCLUDED.question_type,
  options = EXCLUDED.options,
  correct_answer = EXCLUDED.correct_answer,
  explanation = EXCLUDED.explanation,
  points = EXCLUDED.points,
  order_index = EXCLUDED.order_index;