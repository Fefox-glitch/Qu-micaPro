from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QRadioButton, QButtonGroup, QFrame,
                             QMessageBox, QScrollArea, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.database import Database
from src.auth import AuthManager
from datetime import datetime, timedelta

class QuizView(QWidget):
    def __init__(self, database: Database, auth_manager: AuthManager, lesson: dict, quizzes: list, parent_view):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.lesson = lesson
        self.quizzes = quizzes
        self.parent_view = parent_view
        self.current_question_index = 0
        self.score = 0
        self.answers = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        # Header más legible con mayor altura y layout en fila
        header.setStyleSheet(
            "background-color: #4CAF50;"
            "padding: 16px;"
            "border-bottom: 2px solid #3E8E41;"
        )
        header.setFixedHeight(100)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(40, 12, 40, 12)
        header_layout.setSpacing(12)

        title_label = QLabel(f"Cuestionario: {self.lesson['title']}")
        font = QFont("Arial", 22)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: white;")
        # Sombra para mejorar contraste en fondos lisos
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 1)
        title_label.setGraphicsEffect(shadow)

        self.progress_label = QLabel(f"Pregunta 1 de {len(self.quizzes)}")
        self.progress_label.setFont(QFont("Arial", 12))
        self.progress_label.setStyleSheet(
            "color: white;"
            "background-color: rgba(255,255,255,0.18);"
            "border: 1px solid rgba(255,255,255,0.35);"
            "border-radius: 12px;"
            "padding: 6px 10px;"
        )

        header_layout.addWidget(title_label, 1)
        header_layout.addWidget(self.progress_label, 0, Qt.AlignRight)

        header.setLayout(header_layout)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        # Ajuste de margen superior para evitar superposición con header
        self.content_layout.setContentsMargins(60, 36, 60, 40)
        self.content_layout.setSpacing(25)

        self.content_widget.setLayout(self.content_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.content_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        layout.addWidget(header)
        layout.addWidget(scroll)

        self.setLayout(layout)

        self.show_question()

    def show_question(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.current_question_index >= len(self.quizzes):
            self.show_results()
            return

        quiz = self.quizzes[self.current_question_index]

        self.progress_label.setText(f"Pregunta {self.current_question_index + 1} de {len(self.quizzes)}")

        question_card = QFrame()
        question_card.setStyleSheet("""
            QFrame {
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 25px;
            }
        """)

        question_layout = QVBoxLayout()

        question_label = QLabel(quiz['question'])
        font = QFont("Arial", 16)
        font.setBold(True)
        question_label.setFont(font)
        question_label.setStyleSheet("color: #1e3c72;")
        question_label.setWordWrap(True)

        question_layout.addWidget(question_label)
        question_card.setLayout(question_layout)

        self.content_layout.addWidget(question_card)

        options_label = QLabel("Selecciona tu respuesta:")
        options_label.setFont(QFont("Arial", 13))
        options_label.setStyleSheet("color: #666; margin-top: 15px;")
        self.content_layout.addWidget(options_label)

        self.button_group = QButtonGroup()

        if quiz['question_type'] in ['multiple_choice', 'true_false']:
            options = quiz['options']
            for i, option in enumerate(options):
                radio = QRadioButton(option)
                radio.setFont(QFont("Arial", 13))
                radio.setStyleSheet("""
                    QRadioButton {
                        padding: 12px;
                        color: #333;
                    }
                    QRadioButton::indicator {
                        width: 20px;
                        height: 20px;
                    }
                """)
                self.button_group.addButton(radio, i)
                self.content_layout.addWidget(radio)

        self.content_layout.addStretch()

        button_layout = QHBoxLayout()

        if self.current_question_index > 0:
            back_btn = QPushButton("← Anterior")
            back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9E9E9E;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 25px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #757575;
                }
            """)
            back_btn.setCursor(Qt.PointingHandCursor)
            back_btn.clicked.connect(self.previous_question)
            button_layout.addWidget(back_btn)

        button_layout.addStretch()

        next_btn = QPushButton("Siguiente →" if self.current_question_index < len(self.quizzes) - 1 else "Finalizar")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        next_btn.setCursor(Qt.PointingHandCursor)
        next_btn.clicked.connect(self.next_question)
        button_layout.addWidget(next_btn)

        self.content_layout.addLayout(button_layout)

        if self.current_question_index in self.answers:
            saved_answer = self.answers[self.current_question_index]
            quiz = self.quizzes[self.current_question_index]
            options = quiz['options']
            if saved_answer in options:
                index = options.index(saved_answer)
                button = self.button_group.button(index)
                if button:
                    button.setChecked(True)

    def next_question(self):
        selected_button = self.button_group.checkedButton()

        if not selected_button:
            QMessageBox.warning(self, "Respuesta requerida", "Por favor selecciona una respuesta antes de continuar.")
            return

        button_id = self.button_group.id(selected_button)
        quiz = self.quizzes[self.current_question_index]
        selected_answer = quiz['options'][button_id]

        self.answers[self.current_question_index] = selected_answer

        self.current_question_index += 1
        self.show_question()

    def previous_question(self):
        self.current_question_index -= 1
        self.show_question()

    def show_results(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.progress_label.setText("Resultados")

        correct_answers = 0
        total_points = 0
        earned_points = 0

        for i, quiz in enumerate(self.quizzes):
            total_points += quiz['points']
            if i in self.answers:
                if self.answers[i] == quiz['correct_answer']:
                    correct_answers += 1
                    earned_points += quiz['points']

        percentage = int((earned_points / total_points) * 100) if total_points > 0 else 0

        result_card = QFrame()
        result_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4CAF50, stop:1 #45a049);
                border-radius: 15px;
                padding: 40px;
            }
        """)

        result_layout = QVBoxLayout()
        result_layout.setAlignment(Qt.AlignCenter)

        emoji = "🏆" if percentage >= 90 else "⭐" if percentage >= 70 else "📚"

        emoji_label = QLabel(emoji)
        emoji_label.setFont(QFont("Arial", 64))
        emoji_label.setStyleSheet("color: white;")
        emoji_label.setAlignment(Qt.AlignCenter)

        score_label = QLabel(f"{percentage}%")
        font = QFont("Arial", 48)
        font.setBold(True)
        score_label.setFont(font)
        score_label.setStyleSheet("color: white;")
        score_label.setAlignment(Qt.AlignCenter)

        result_text = "¡Excelente trabajo!" if percentage >= 90 else "¡Buen trabajo!" if percentage >= 70 else "Sigue practicando"
        result_label = QLabel(result_text)
        result_label.setFont(QFont("Arial", 20))
        result_label.setStyleSheet("color: white;")
        result_label.setAlignment(Qt.AlignCenter)

        stats_label = QLabel(f"Respuestas correctas: {correct_answers}/{len(self.quizzes)}")
        stats_label.setFont(QFont("Arial", 14))
        stats_label.setStyleSheet("color: white;")
        stats_label.setAlignment(Qt.AlignCenter)

        result_layout.addWidget(emoji_label)
        result_layout.addWidget(score_label)
        result_layout.addWidget(result_label)
        result_layout.addSpacing(10)
        result_layout.addWidget(stats_label)

        result_card.setLayout(result_layout)
        self.content_layout.addWidget(result_card)

        self.content_layout.addSpacing(30)

        review_label = QLabel("Revisión de Respuestas")
        font = QFont("Arial", 18)
        font.setBold(True)
        review_label.setFont(font)
        review_label.setStyleSheet("color: #1e3c72;")
        self.content_layout.addWidget(review_label)

        for i, quiz in enumerate(self.quizzes):
            review_card = self.create_review_card(i, quiz)
            self.content_layout.addWidget(review_card)

        self.content_layout.addStretch()

        finish_btn = QPushButton("Finalizar")
        finish_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 40px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        finish_btn.setCursor(Qt.PointingHandCursor)
        finish_btn.clicked.connect(self.finish_quiz)
        self.content_layout.addWidget(finish_btn, alignment=Qt.AlignCenter)

        user_id = self.auth.get_current_user_id()
        self.db.save_lesson_progress(user_id, self.lesson['id'], True, percentage)

        self.check_achievements(percentage)

    def create_review_card(self, index: int, quiz: dict) -> QFrame:
        user_answer = self.answers.get(index, "Sin respuesta")
        is_correct = user_answer == quiz['correct_answer']

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {'#e8f5e9' if is_correct else '#ffebee'};
                border-left: 4px solid {'#4CAF50' if is_correct else '#f44336'};
                border-radius: 8px;
                padding: 20px;
            }}
        """)

        layout = QVBoxLayout()

        question_label = QLabel(f"{index + 1}. {quiz['question']}")
        font = QFont("Arial", 13)
        font.setBold(True)
        question_label.setFont(font)
        question_label.setStyleSheet("color: #333;")
        question_label.setWordWrap(True)

        your_answer_label = QLabel(f"Tu respuesta: {user_answer}")
        your_answer_label.setFont(QFont("Arial", 12))
        your_answer_label.setStyleSheet(f"color: {'#4CAF50' if is_correct else '#f44336'};")

        if not is_correct:
            correct_answer_label = QLabel(f"Respuesta correcta: {quiz['correct_answer']}")
            font = QFont("Arial", 12)
            font.setBold(True)
            correct_answer_label.setFont(font)
            correct_answer_label.setStyleSheet("color: #4CAF50;")

        explanation_label = QLabel(f"Explicación: {quiz['explanation']}")
        explanation_label.setFont(QFont("Arial", 11))
        explanation_label.setStyleSheet("color: #666;")
        explanation_label.setWordWrap(True)

        layout.addWidget(question_label)
        layout.addWidget(your_answer_label)
        if not is_correct:
            layout.addWidget(correct_answer_label)
        layout.addWidget(explanation_label)

        card.setLayout(layout)
        return card

    def check_achievements(self, percentage: int):
        user_id = self.auth.get_current_user_id()
        achievements = self.db.get_all_achievements()
        progress = self.db.get_user_progress(user_id)
        any_awarded = False
        completed_lessons = sum(1 for p in progress if p['completed'])

        for achievement in achievements:
            if achievement['requirement_type'] == 'lesson_complete' and completed_lessons >= achievement['requirement_value']:
                awarded = self.db.award_achievement(user_id, achievement['id'])
                if awarded:
                    any_awarded = True
                    QMessageBox.information(self, "🏆 ¡Logro Desbloqueado!",
                                          f"{achievement['title']}\n\n{achievement['description']}")

            elif achievement['requirement_type'] == 'perfect_score' and percentage >= achievement['requirement_value']:
                awarded = self.db.award_achievement(user_id, achievement['id'])
                if awarded:
                    any_awarded = True
                    QMessageBox.information(self, "🏆 ¡Logro Desbloqueado!",
                                          f"{achievement['title']}\n\n{achievement['description']}")

        # Calcular racha diaria de aprendizaje (días consecutivos con al menos una lección completada)
        dates = []
        for p in progress:
            if p.get('completed') and p.get('completed_at'):
                try:
                    dt = datetime.fromisoformat(p['completed_at'])
                    dates.append(dt.date())
                except Exception:
                    pass
        unique_dates = sorted(set(dates))
        max_streak = 0
        current_streak = 0
        prev_date = None
        for d in unique_dates:
            if prev_date is None or d == prev_date + timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)
            prev_date = d

        for achievement in achievements:
            if achievement['requirement_type'] == 'streak' and max_streak >= achievement['requirement_value']:
                awarded = self.db.award_achievement(user_id, achievement['id'])
                if awarded:
                    any_awarded = True
                    QMessageBox.information(self, "🏆 ¡Logro Desbloqueado!",
                                          f"{achievement['title']}\n\n{achievement['description']}")

        modules = self.db.get_all_modules()
        for module in modules:
            completion = self.db.get_module_completion(user_id, module['id'])
            if completion['percentage'] == 100:
                matching_achievements = [a for a in achievements
                                       if a['requirement_type'] == 'module_complete'
                                       and a['requirement_value'] == module['id']]
                for achievement in matching_achievements:
                    awarded = self.db.award_achievement(user_id, achievement['id'])
                    if awarded:
                        any_awarded = True
                        QMessageBox.information(self, "🏆 ¡Logro Desbloqueado!",
                                              f"{achievement['title']}\n\n{achievement['description']}")

        # Notificar ventana principal si hay nuevos logros
        try:
            main_window = self.window()
            if hasattr(main_window, 'notify_achievement_awarded') and any_awarded:
                main_window.notify_achievement_awarded()
        except Exception:
            pass

    def finish_quiz(self):
        self.parent_view.return_to_module()
