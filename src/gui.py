# gui.py

import sys
import os
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QDialog, QMessageBox, QProgressDialog, QFileDialog)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from matrix_operations import pad_matrix, strassen, add_matrix, subtract_matrix
from analytics import show_analytics

class StrassenGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Strassen's Matrix Multiplication")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(self.load_stylesheet())
        self.initUI()

    def load_stylesheet(self):
        return """
        QWidget {
            font-family: Arial, sans-serif;
            font-size: 14px;
            background-color: #f0f0f0;
        }
        QTextEdit {
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLabel {
            font-weight: bold;
            color: #333;
        }
        QDialog {
            background-color: #f0f0f0;
        }
        """

    def initUI(self):
        main_layout = QVBoxLayout()

        # Input fields for matrices
        input_layout = QHBoxLayout()
        self.matrix1_input = QTextEdit()
        self.matrix1_input.setToolTip("Enter Matrix A in the format: [[1, 2], [3, 4]]")
        self.matrix2_input = QTextEdit()
        self.matrix2_input.setToolTip("Enter Matrix B in the format: [[1, 2], [3, 4]]")
        input_layout.addWidget(QLabel("Matrix A:"))
        input_layout.addWidget(self.matrix1_input)
        input_layout.addWidget(QLabel("Matrix B:"))
        input_layout.addWidget(self.matrix2_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.multiply_button = QPushButton("Multiply")
        self.multiply_button.setIcon(QIcon(os.path.join("icons", "multiply_icon.png")))
        self.multiply_button.setToolTip("Click to multiply the matrices")
        self.multiply_button.clicked.connect(self.multiply_matrices)
        button_layout.addWidget(self.multiply_button)

        self.show_process_button = QPushButton("Show Process")
        self.show_process_button.setIcon(QIcon(os.path.join("icons", "process_icon.png")))
        self.show_process_button.setToolTip("Click to show the calculation process")
        self.show_process_button.clicked.connect(self.show_process)
        button_layout.addWidget(self.show_process_button)

        self.show_analytics_button = QPushButton("Show Analytics")
        self.show_analytics_button.setIcon(QIcon(os.path.join("icons", "analytics_icon.png")))
        self.show_analytics_button.setToolTip("Click to show time complexity analytics")
        self.show_analytics_button.clicked.connect(self.show_analytics)
        button_layout.addWidget(self.show_analytics_button)

        self.help_button = QPushButton("Help")
        self.help_button.setIcon(QIcon(os.path.join("icons", "help_icon.png")))
        self.help_button.setToolTip("Click for help")
        self.help_button.clicked.connect(self.show_help)
        button_layout.addWidget(self.help_button)

        self.save_button = QPushButton("Save Matrices")
        self.save_button.setIcon(QIcon(os.path.join("icons", "save_icon.png")))
        self.save_button.setToolTip("Click to save the matrices to a file")
        self.save_button.clicked.connect(self.save_matrices)
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Matrices")
        self.load_button.setIcon(QIcon(os.path.join("icons", "load_icon.png")))
        self.load_button.setToolTip("Click to load matrices from a file")
        self.load_button.clicked.connect(self.load_matrices)
        button_layout.addWidget(self.load_button)

        self.export_button = QPushButton("Export Results")
        self.export_button.setIcon(QIcon(os.path.join("icons", "export_icon.png")))
        self.export_button.setToolTip("Click to export the results to a file")
        self.export_button.clicked.connect(self.export_results)
        button_layout.addWidget(self.export_button)

        # Result display
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("Result:"))
        main_layout.addWidget(self.result_output)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def get_matrix_from_input(self, input_text):
        try:
            matrix = np.array(eval(input_text))
            if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
                raise ValueError("Matrix must be square.")
            if (matrix.shape[0] & (matrix.shape[0] - 1)) != 0:
                raise ValueError("Matrix size must be 2^n x 2^n.")
            return matrix
        except Exception as e:
            QMessageBox.critical(self, "Input Error", f"Invalid matrix input: {e}")
            return None

    def multiply_matrices(self):
        A = self.get_matrix_from_input(self.matrix1_input.toPlainText())
        B = self.get_matrix_from_input(self.matrix2_input.toPlainText())

        if A is not None and B is not None:
            if A.shape == B.shape and A.shape[0] == A.shape[1]:
                A_padded = pad_matrix(A)
                B_padded = pad_matrix(B)
                progress = QProgressDialog("Multiplying matrices...", "Cancel", 0, 100, self)
                progress.setWindowModality(Qt.WindowModality.WindowModal)
                progress.setValue(0)
                progress.show()

                result_padded = strassen(A_padded, B_padded)
                result = result_padded[:A.shape[0], :A.shape[1]]
                self.result_output.setText(str(result))

                progress.setValue(100)
            else:
                QMessageBox.critical(self, "Input Error", "Matrices must be square and of the same size")

    def show_process(self):
        process_dialog = QDialog(self)
        process_dialog.setWindowTitle("Calculation Process")
        process_dialog.setGeometry(100, 100, 600, 400)

        process_text = QTextEdit(process_dialog)
        process_text.setReadOnly(True)
        process_text.setText("Detailed steps of the calculation will be shown here...")

        layout = QVBoxLayout()
        layout.addWidget(process_text)
        process_dialog.setLayout(layout)
        process_dialog.exec()

    def show_analytics(self):
        show_analytics()

    def show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Help")
        help_dialog.setGeometry(100, 100, 600, 400)

        help_text = QTextEdit(help_dialog)
        help_text.setReadOnly(True)
        help_text.setText("""
        How to Use the Application:
        1. Enter Matrix A in the format: [[1, 2], [3, 4]]
        2. Enter Matrix B in the format: [[1, 2], [3, 4]]
        3. Click the "Multiply" button to perform the multiplication.
        4. Click the "Show Process" button to view the detailed steps of the calculation.
        5. Click the "Show Analytics" button to view the time complexity comparison between conventional and Strassen's algorithms.
        6. Use the "Save Matrices" button to save the current matrices to a file.
        7. Use the "Load Matrices" button to load matrices from a file.
        8. Use the "Export Results" button to export the multiplication results to a CSV file.
        """)

        layout = QVBoxLayout()
        layout.addWidget(help_text)
        help_dialog.setLayout(layout)
        help_dialog.exec()

    def save_matrices(self):
        options = QFileDialog.ptions()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Matrices", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write("Matrix A:\n")
                file.write(self.matrix1_input.toPlainText() + "\n")
                file.write("Matrix B:\n")
                file.write(self.matrix2_input.toPlainText() + "\n")

    def load_matrices(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Matrices", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                matrices = content.split("Matrix B:\n")
                self.matrix1_input.setText(matrices[0].replace("Matrix A:\n", "").strip())
                self.matrix2_input.setText(matrices[1].strip())

    def export_results(self):
        options = QFileDialog.options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            result_text = self.result_output.toPlainText()
            try:
                result_matrix = eval(result_text)
                df = pd.DataFrame(result_matrix)
                df.to_csv(file_name, index=False)
                QMessageBox.information(self, "Export Successful", "Results have been successfully exported.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export results: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StrassenGUI()
    window.show()
    sys.exit(app.exec())