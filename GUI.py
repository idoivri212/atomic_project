import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QFormLayout, QLineEdit, QMessageBox, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from cascade import Cascade
import datetime


class CentrifugeRowSelectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        title = QLabel("Centrifuge Cascade Simulation")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: red;")  # Bright color for the title
        main_layout.addWidget(title)

        form_layout = QFormLayout()

        """        self.stripper_row_combo = QLineEdit()
        self.stripper_row_combo.setPlaceholderText("Select number of Stripper rows")
        form_layout.addRow(self.stripper_row_combo)"""

        self.label1 = QLabel("Cascade Parameters")
        self.label1.setStyleSheet("font-size:20px;")
        form_layout.addRow(self.label1)

        self.rectifier_row_combo = QLineEdit()
        self.rectifier_row_combo.setPlaceholderText("N. Rows")

        self.alpha = QLineEdit()
        self.alpha.setPlaceholderText("α")

        self.Q = QLineEdit()
        self.Q.setPlaceholderText("Q")

        param_line = QHBoxLayout()
        param_line.addWidget(self.rectifier_row_combo)
        param_line.addWidget(self.alpha)
        param_line.addWidget(self.Q)

        form_layout.addRow(param_line)

        self.label2 = QLabel("Enrichment Parameters")
        self.label2.setStyleSheet("font-size:20px;")
        form_layout.addRow(self.label2)

        self.concentration = QLineEdit()
        self.concentration.setPlaceholderText("Input concentration")
        self.flow = QLineEdit()
        self.flow.setPlaceholderText("Input flow")
        flow_line = QHBoxLayout()
        flow_line.addWidget(self.concentration)
        flow_line.addWidget(self.flow)
        form_layout.addRow(flow_line)

        self.goal = QLineEdit()
        self.goal.setPlaceholderText("Concentration goal")
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Desired amount")
        goal_line = QHBoxLayout()
        goal_line.addWidget(self.goal)
        goal_line.addWidget(self.amount)
        form_layout.addRow(goal_line)

        main_layout.addLayout(form_layout)

        self.next_button = QPushButton('Next')
        self.next_button.setFont(QFont('Arial', 20))
        self.next_button.setStyleSheet("background-color: red; color: white; padding: 10px; margin: 20px;")
        self.next_button.clicked.connect(self.openCentrifugeSelectionWindow)
        main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.setWindowTitle('Centrifuge Row Selection')
        self.setStyleSheet("""
            QWidget { background-color: #2E2E2E; color: white; }
            QLineEdit { margin: 10px; padding:10px; font-size: 14px;}
        """)
        self.setFixedSize(800, 600)
        self.show()

    def openCentrifugeSelectionWindow(self):
        # TODO: check if all entries are full
        # stripper_rows = int(self.stripper_row_combo.text())
        try:
            rectifier_rows = int(self.rectifier_row_combo.text())
            cent_params = float(self.alpha.text()), float(self.Q.text())
            flow = float(self.concentration.text()), float(self.flow.text())
            goal = float(self.goal.text()), float(self.amount.text())
            self.centrifuge_selection_window = CentrifugeSelectionApp(rectifier_rows, cent_params, flow,goal)
            self.centrifuge_selection_window.show()
            self.close()
        except Exception as e:
            print(e)
            QMessageBox.critical(self, 'Error', "Please fill in all fields!")


class CentrifugeSelectionApp(QWidget):
    def __init__(self, rect_rows, cent_params, flow, goal):
        super().__init__()
        # self.stripper_rows = stripper_rows
        self.cent_params = cent_params
        self.flow = flow
        self.goal = goal
        self.rectifier_rows = rect_rows
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        title = QLabel("Centrifuge Cascade Configuration")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: red; padding: 30px;")  # Bright color for the title
        main_layout.addWidget(title, alignment=Qt.AlignCenter)
        config_layout = QHBoxLayout()

        # Stripper Configuration
        """        stripper_layout = QFormLayout()
        self.stripper_inputs = []
        stripper_panel = QVBoxLayout()
        stripper_title = QLabel('Stripper')
        stripper_title.setAlignment(Qt.AlignCenter)
        stripper_title.setFont(QFont('Arial', 14, QFont.Bold))
        stripper_panel.addWidget(stripper_title, alignment=Qt.AlignTop)
        for i in range(self.stripper_rows):
            centrifuge_count = QLineEdit()
            centrifuge_count.setPlaceholderText(f'Row {i + 1}')
            centrifuge_count.setAlignment(Qt.AlignTop)
            centrifuge_count.textChanged.connect(self.updateCascade)
            self.stripper_inputs.append(centrifuge_count)
            stripper_layout.addRow(centrifuge_count)
        stripper_panel.addLayout(stripper_layout)
        config_layout.addLayout(stripper_panel)"""

        # Rectifier Configuration
        rectifier_layout = QFormLayout()
        self.rectifier_inputs = []
        rectifier_panel = QVBoxLayout()
        rectifier_title = QLabel('Rectifier')
        rectifier_title.setAlignment(Qt.AlignCenter)
        rectifier_title.setFont(QFont('Arial', 14, QFont.Bold))
        rectifier_panel.addWidget(rectifier_title, alignment=Qt.AlignTop)
        for i in range(self.rectifier_rows):
            centrifuge_count = QLineEdit()
            centrifuge_count.setPlaceholderText(f'Row {i + 1}')
            centrifuge_count.setAlignment(Qt.AlignTop)
            centrifuge_count.textChanged.connect(self.updateCascade)
            self.rectifier_inputs.append(centrifuge_count)
            rectifier_layout.addRow(centrifuge_count)
        rectifier_panel.addLayout(rectifier_layout)
        config_layout.addLayout(rectifier_panel)

        # Cascade Visualization
        self.cascade_grid = QGridLayout()
        self.cascade_display = QWidget()
        self.cascade_display.setLayout(self.cascade_grid)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.cascade_display)
        scroll_area.setFixedSize(400, 400)  # Fixed size for consistent display

        config_layout.addWidget(scroll_area)

        main_layout.addLayout(config_layout)

        # Run Simulation Button
        self.run_button = QPushButton('Run')
        self.run_button.setFont(QFont('Arial', 14))
        self.run_button.setStyleSheet("background-color: red; color: white; padding: 10px; margin: 20px;")
        self.run_button.clicked.connect(self.runSimulation)
        main_layout.addWidget(self.run_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.setWindowTitle('Centrifuge Configuration')
        self.setStyleSheet("""
            QWidget { background-color: #2E2E2E; color: white; }
            QLineEdit { margin: 5px; padding: 5px; background-color: #3E3E3E; color: white; border: 1px solid #5E5E5E; }
        """)
        self.show()

    def updateCascade(self):
        for i in reversed(range(self.cascade_grid.count())):
            self.cascade_grid.itemAt(i).widget().setParent(None)

        # Update Stripper Visualization
        """        for i, input_field in enumerate(self.stripper_inputs):
            try:
                count = int(input_field.text())
            except ValueError:
                count = 0
            for j in range(count):
                label = QLabel('C')
                label.setFixedSize(20, 20)  # Smaller size for better fitting
                label.setStyleSheet("background-color: lightblue; padding: 5px; border: 1px solid black;")
                label.setAlignment(Qt.AlignCenter)
                self.cascade_grid.addWidget(label, i, j, alignment=Qt.AlignCenter)"""

        # Update Rectifier Visualization
        # start_row = len(self.stripper_inputs)
        start_row = 0
        for i, input_field in enumerate(self.rectifier_inputs):
            try:
                count = int(input_field.text())
            except ValueError:
                count = 0
            for j in range(count):
                label = QLabel('C')
                label.setFixedSize(20, 20)  # Smaller size for better fitting
                label.setStyleSheet("background-color: lightgreen; padding: 5px; border: 1px solid black;")
                label.setAlignment(Qt.AlignCenter)
                self.cascade_grid.addWidget(label, start_row + i, j, alignment=Qt.AlignCenter)

    def runSimulation(self):
        # Collect Stripper configurations
        """        stripper_config = []
        for input_field in self.stripper_inputs:
            text = input_field.text().strip()
            if text:
                try:
                    stripper_config.append(int(text))
                except ValueError:
                    QMessageBox.critical(self, 'Error', f"Invalid input '{text}' in Stripper configuration. Please enter a valid integer.")
                    return
            else:
                QMessageBox.critical(self, 'Error', "Please fill in all fields in Stripper configuration.")
                return"""

        # Collect Rectifier configurations
        rectifier_config = []
        for input_field in self.rectifier_inputs:
            text = input_field.text().strip()
            if text:
                try:
                    rectifier_config.append(int(text))
                except ValueError:
                    QMessageBox.critical(self, 'Error', f"Invalid input '{text}' in Rectifier configuration. Please enter a valid integer.")
                    return
            else:
                QMessageBox.critical(self, 'Error', "Please fill in all fields in Rectifier configuration.")
                return

        # Placeholder for actual simulation logic

        # Display results in a message box
        try:
            cascade = Cascade(rectifier_config, self.cent_params, self.flow, self.goal)
            cascade.run()
            min = int(cascade.breakout_time*60)
            QMessageBox.information(self, 'Simulation Results', f"Breakout time is: {min // (24*60)} Days, {(min % (24*60)) // 60} Hours and {min % 60} Minuets")

            self.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CentrifugeRowSelectionApp()
    sys.exit(app.exec_())
