from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QMessageBox,
)
from PyQt6.QtGui import QFont
import sys


class DietRecommendationApp(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Personalized Diet Recommendation System")
        # self.setGeometry(0, 0, 870, 690)
        # self.selected_goal = None
        # self.initUI()
        self.setWindowTitle("Personalized Diet Recommendation System")
        window_width = 870
        window_height = 690
        app_bg = "#457044"
        app_text_bg = "#e9ffcf"
        # app_bg = "#4bcbee"
        self.setStyleSheet(f"background-color:{app_bg}; color:{app_text_bg};")
        self.setFixedSize(window_width, window_height)
        self.center_window()
        self.selected_goal = None
        self.initUI()

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()  # Get screen size
        window_geometry = self.geometry()  # Get window size

        center_x = (screen_geometry.width() - window_geometry.width()) // 2
        center_y = (screen_geometry.height() - window_geometry.height()) // 2

        self.move(center_x, center_y - 30)  # Move window to the center

    def initUI(self):
        app_left = 50
        app_right = 50
        font = QFont("Arial", 14)
        title_font = QFont("Arial", 32, QFont.Weight.Bold)

        layout = QVBoxLayout()

        self.title_label = QLabel("DIETIFY")
        # self.title_label.setStyleSheet("color:white")
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)

        self.project_label = QLabel("PERSONALIZED DIET RECOMMENDATION SYSTEM")
        self.project_label.setFont(font)
        layout.addWidget(self.project_label)

        # Age Input
        self.age_label = QLabel("AGE")
        self.age_label.setFont(font)
        layout.addWidget(self.age_label)

        self.age_input = QLineEdit()
        self.age_input.setFont(font)
        layout.addWidget(self.age_input)

        # Height Input
        self.height_label = QLabel("HEIGHT IN CM")
        self.height_label.setFont(font)
        layout.addWidget(self.height_label)

        self.height_input = QLineEdit()
        self.height_input.setFont(font)
        self.height_input.textChanged.connect(self.calculate_bmi)
        layout.addWidget(self.height_input)

        # Weight Input
        self.weight_label = QLabel("WEIGHT IN KG")
        self.weight_label.setFont(font)
        layout.addWidget(self.weight_label)

        self.weight_input = QLineEdit()
        self.weight_input.setFont(font)
        self.weight_input.textChanged.connect(self.calculate_bmi)
        layout.addWidget(self.weight_input)

        # BMI Label
        self.bmi_label = QLabel("BMI: ")
        self.bmi_label.setFont(font)
        layout.addWidget(self.bmi_label)

        # Diet Type
        self.diet_type_label = QLabel("DIET TYPE")
        self.diet_type_label.setFont(font)
        layout.addWidget(self.diet_type_label)

        self.diet_type = QComboBox()
        self.diet_type.addItems(["All", "Veg", "Non-Veg"])
        self.diet_type.setFont(font)
        layout.addWidget(self.diet_type)

        # Fitness Goal Selection
        self.goal_label = QLabel("FITNESS GOAL")
        self.goal_label.setFont(font)
        layout.addWidget(self.goal_label)

        self.goal_buttons_layout = QHBoxLayout()
        self.goal_buttons = []
        goals = ["Weight Loss", "Muscle Gain", "Healthy"]
        for goal in goals:
            button = QPushButton(goal)
            button.setFont(font)
            button.clicked.connect(lambda checked, g=goal: self.select_goal(g))
            self.goal_buttons.append(button)
            self.goal_buttons_layout.addWidget(button)
        layout.addLayout(self.goal_buttons_layout)

        # Submit Button
        self.submit_button = QPushButton("OUTPUT")
        self.submit_button.setFont(font)
        self.submit_button.clicked.connect(self.get_user_inputs)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def select_goal(self, goal):
        self.selected_goal = goal
        for button in self.goal_buttons:
            if button.text() == goal:
                button.setStyleSheet("background-color: #00ffdd; color: black;")
            else:
                button.setStyleSheet("background-color: #ddf2c4; color: black;")

    def calculate_bmi(self):
        try:
            height = float(self.height_input.text()) / 100
            weight = float(self.weight_input.text())
            bmi = weight / (height**2)
            self.bmi_label.setText(f"BMI: {bmi:.2f}")
        except ValueError:
            self.bmi_label.setText("BMI: ")

    def get_user_inputs(self):
        user_age = self.age_input.text()
        user_height = self.height_input.text()
        user_weight = self.weight_input.text()
        user_bmi = self.bmi_label.text()
        user_diet_type = self.diet_type.currentText()
        user_fitness_goal = self.selected_goal if self.selected_goal else "None"

        msg = f"Age: {user_age}\nHeight: {user_height}\nWeight: {user_weight}\nBMI: {user_bmi}\nDiet Type: {user_diet_type}\nFitness Goal: {user_fitness_goal}"
        print(msg)
        # QMessageBox.information(self, "User Inputs", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DietRecommendationApp()
    window.show()
    sys.exit(app.exec())
