-- Inserta/actualiza quizzes adicionales para la lección 7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767
-- Usa ON CONFLICT para permitir re-ejecuciones sin fallar por duplicados

INSERT INTO "public"."quizzes" (
  "id","lesson_id","question","question_type","options","correct_answer","explanation","points","order_index"
) VALUES
 ('f126f8eb-21b0-4c40-a75c-2892f12cd421','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué es un elemento químico?','multiple_choice','["Una sustancia pura formada por un solo tipo de átomo","Una mezcla de átomos","Dos sustancias unidas","Un tipo de energía"]','Una sustancia pura formada por un solo tipo de átomo','Un elemento químico está formado solo por un tipo de átomo.',10,6),
 ('4a1b3453-6f6e-4f2f-9baf-f946fd7a99d7','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es el símbolo químico del sodio?','multiple_choice','["So","Sd","Na","S"]','Na','El símbolo del sodio proviene del latín “Natrium”.',10,7),
 ('c9d67dcf-f7c6-49bc-9a4a-33c0f6cf5a11','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué partícula del átomo no tiene carga eléctrica?','multiple_choice','["Protón","Electrón","Neutrón","Ion"]','Neutrón','El neutrón es eléctricamente neutro.',10,8),
 ('1c0df8d0-b8be-4e1e-acf4-1f4e4461925c','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué subpartícula se encuentra alrededor del núcleo?','multiple_choice','["Protones","Electrones","Neutrones","Todas"]','Electrones','Los electrones se encuentran girando alrededor del núcleo atómico.',10,9),
 ('43584836-713c-4633-8406-6b7fb0b862bd','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es el estado gaseoso del agua?','multiple_choice','["Lluvia","Nube","Vapor","Hielo"]','Vapor','El agua en estado gaseoso es vapor.',10,10),
 ('9e13d6d2-d371-45c8-8a83-b56a6b8cf0b7','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué tipo de cambio es la fusión del hielo?','multiple_choice','["Químico","Nuclear","Físico","Iónico"]','Físico','La fusión es un cambio físico: no altera la composición del agua.',10,11),
 ('03d20ff0-d223-405c-a20b-3fb93c891a43','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es el gas más abundante en la atmósfera?','multiple_choice','["Oxígeno","Dióxido de carbono","Nitrógeno","Hidrógeno"]','Nitrógeno','El 78% del aire es nitrógeno.',10,12),
 ('800012a5-940c-4a88-bef6-b96dcb1b3201','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué describe el número atómico?','multiple_choice','["Electrones totales","Protones del átomo","Neutrones del núcleo","Masa total"]','Protones del átomo','El número atómico indica la cantidad de protones.',10,13),
 ('14fd9c86-3b2c-4bb5-bdd2-d4eae4aef331','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es la molécula del oxígeno respirable?','multiple_choice','["O","O₂","CO₂","O₃"]','O₂','El oxígeno que respiramos es O₂.',10,14),
 ('e3da9bc7-6d8d-41e7-866e-a666ca55f50b','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué indica la masa atómica?','multiple_choice','["Número de protones","Suma de protones y neutrones","Número de electrones","Número de moléculas"]','Suma de protones y neutrones','La masa atómica es protones + neutrones.',10,15),
 ('c3dcfecc-35c9-4dd2-866e-c78fcd4d14fa','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es el símbolo del carbono?','multiple_choice','["Co","Ca","C","Cb"]','C','El símbolo del carbono es C.',10,16),
 ('8f1e45fe-a274-4ce8-bcbe-fda3c1bc9e24','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué tipo de sustancia es el aire?','multiple_choice','["Elemento","Mezcla","Compuesto","Molécula"]','Mezcla','El aire es una mezcla de gases.',10,17),
 ('f418f6fa-90cb-49a5-bd29-7239b13c9879','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','El hierro se oxida. ¿Qué tipo de cambio es?','multiple_choice','["Físico","Químico","Nuclear","Eléctrico"]','Químico','La oxidación transforma químicamente el hierro.',10,18),
 ('21061231-9d0b-4e67-b3c9-9ee573c8e151','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es el símbolo del hidrógeno?','multiple_choice','["Hy","Hd","H","He"]','H','El hidrógeno se representa con H.',10,19),
 ('b7bf0684-1438-4217-a66d-23513887c6fb','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué sucede al hervir agua?','multiple_choice','["Cambio químico","Cambio físico","Se forman nuevos elementos","Se destruyen moléculas"]','Cambio físico','Solo cambia de líquido a gas, sin alterar su composición.',10,20),
 ('1b18fa54-d5aa-4da7-8bea-3d9c7db67a86','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Cuál es la fórmula del dióxido de carbono?','multiple_choice','["CO","C₂","CO₂","O₂C"]','CO₂','El dióxido de carbono es CO₂.',10,21),
 ('6de30e53-d14f-4b0a-ae1c-e369d148e186','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué estado de la materia tiene forma variable pero volumen fijo?','multiple_choice','["Sólido","Líquido","Gas","Plasma"]','Líquido','Los líquidos tienen volumen fijo pero forma variable.',10,22),
 ('0cb2318c-b38d-4f8d-9a31-1f52696d5285','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué es una mezcla homogénea?','multiple_choice','["Componentes visibles","Mezcla uniforme","Solo sólidos","No se puede separar"]','Mezcla uniforme','Una mezcla homogénea se ve igual en toda su composición.',10,23),
 ('33b0e12e-0405-4725-98aa-3fe32eab2e54','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','¿Qué indica el pH?','multiple_choice','["Temperatura","Acidez o basicidad","Densidad","Conductividad"]','Acidez o basicidad','El pH mide qué tan ácido o básico es algo.',10,24),
 ('1a7b63b7-cc84-4df8-a713-a48b2b7b5510','7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767','El agua salada es un ejemplo de:','multiple_choice','["Elemento","Mezcla homogénea","Compuesto","Solvente puro"]','Mezcla homogénea','El agua salada es una mezcla uniforme de agua y sal.',10,25)
ON CONFLICT (id) DO UPDATE SET
  lesson_id = EXCLUDED.lesson_id,
  question = EXCLUDED.question,
  question_type = EXCLUDED.question_type,
  options = EXCLUDED.options,
  correct_answer = EXCLUDED.correct_answer,
  explanation = EXCLUDED.explanation,
  points = EXCLUDED.points,
  order_index = EXCLUDED.order_index;