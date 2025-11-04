import sys
import os

# Asegurar que el paquete 'src' sea importable desde 'project/src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import Database


def main():
    try:
        db = Database()
        quizzes = [
            {
                "id": "b6f4dcb8-67e5-42de-8f64-1a561fc93891",
                "lesson_id": "7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767",
                "question": "¿Qué es un átomo?",
                "question_type": "multiple_choice",
                "options": [
                    "La unidad básica de la materia",
                    "Una molécula",
                    "Una mezcla de sustancias",
                    "Un tipo de energía",
                ],
                "correct_answer": "La unidad básica de la materia",
                "explanation": "Un átomo es la unidad más pequeña de la materia que conserva propiedades químicas.",
                "points": 10,
                "order_index": 1,
            },
            {
                "id": "7a2cbd30-624f-43b9-95e7-51e576ffaf6c",
                "lesson_id": "7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767",
                "question": "¿Cuál es la carga del electrón?",
                "question_type": "multiple_choice",
                "options": ["Positiva", "Negativa", "Neutra", "Depende del átomo"],
                "correct_answer": "Negativa",
                "explanation": "Los electrones tienen carga negativa; los protones positiva y los neutrones no tienen carga.",
                "points": 10,
                "order_index": 2,
            },
            {
                "id": "c92d298c-50cf-4218-bbda-7f4e4c078b45",
                "lesson_id": "7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767",
                "question": "¿Cuál de las siguientes es una molécula?",
                "question_type": "multiple_choice",
                "options": ["O₂", "O", "H", "Ne"],
                "correct_answer": "O₂",
                "explanation": "Una molécula es dos o más átomos unidos; O₂ son dos átomos de oxígeno.",
                "points": 10,
                "order_index": 3,
            },
            {
                "id": "9b7f8f63-2f36-4e0d-94cd-9f2c53a53f66",
                "lesson_id": "7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767",
                "question": "El agua es un ejemplo de:",
                "question_type": "multiple_choice",
                "options": ["Elemento", "Compuesto", "Mezcla", "Energía"],
                "correct_answer": "Compuesto",
                "explanation": "El agua (H₂O) es un compuesto formado por hidrógeno y oxígeno.",
                "points": 10,
                "order_index": 4,
            },
            {
                "id": "e0f57e2a-34b3-42a6-a5f5-dfb24fa72c94",
                "lesson_id": "7908e6dc-b8cd-4bc3-b3cc-cd992c9e1767",
                "question": "¿Qué significa “estado sólido”?",
                "question_type": "multiple_choice",
                "options": [
                    "Forma y volumen fijos",
                    "Volumen fijo pero forma variable",
                    "No tiene forma ni volumen",
                    "Estado de energía",
                ],
                "correct_answer": "Forma y volumen fijos",
                "explanation": "En el estado sólido las partículas están muy juntas y mantienen forma y volumen fijo.",
                "points": 10,
                "order_index": 5,
            },
        ]

        # Upsert para evitar errores si ya existen
        db.supabase.table("quizzes").upsert(quizzes).execute()
        print("Quizzes insertados/actualizados correctamente.")
    except Exception as e:
        print(f"Error insertando quizzes: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()