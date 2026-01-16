import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QPropertyAnimation


# -------------------- CONSTANTS --------------------

WINDOWS_BLUE = "#0078D7"


def build_theme():
    return f"""
    QWidget {{
        background-color: rgba(25,25,25,220);
        color: white;
        font-family: Segoe UI;
    }}

    /* HEADER / DISPLAY */
    QLineEdit {{
        background: {WINDOWS_BLUE};
        color: white;
        border-radius: 14px;
        padding: 18px;
        font-size: 30px;
        font-weight: 500;
    }}

    QPushButton {{
        background: rgba(60,60,60,200);
        border-radius: 18px;
        font-size: 22px;
        padding: 18px;
    }}

    QPushButton:hover {{
        background: {WINDOWS_BLUE};
    }}

    QPushButton:pressed {{
        background: {WINDOWS_BLUE};
    }}
    """


# -------------------- MAIN APP --------------------

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.resize(400, 520)
        self.setFocusPolicy(Qt.StrongFocus)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(12)

        # ---- HEADER ----
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.display)

        self.create_buttons()
        self.apply_theme()

    # ---------------- BUTTONS ----------------

    def create_buttons(self):
        keys = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"]
        ]

        for row in keys:
            h = QHBoxLayout()
            for k in row:
                b = QPushButton(k)
                b.clicked.connect(lambda _, t=k: self.on_input(t))
                self.animate_button(b)
                h.addWidget(b)
            self.layout.addLayout(h)

        bottom = QHBoxLayout()

        clear = QPushButton("Clear")
        clear.clicked.connect(self.clear)
        bottom.addWidget(clear)

        copy = QPushButton("Copy")
        copy.clicked.connect(self.copy_result)
        bottom.addWidget(copy)

        self.layout.addLayout(bottom)

    # ---------------- LOGIC ----------------

    def on_input(self, text):
        if text == "=":
            self.calculate()
        else:
            self.display.setText(self.display.text() + text)

    def calculate(self):
        try:
            expr = self.display.text().replace("×", "*").replace("÷", "/")
            self.display.setText(str(eval(expr)))
        except:
            self.display.setText("Error")

    def clear(self):
        self.display.clear()

    def copy_result(self):
        QApplication.clipboard().setText(self.display.text())

    # ---------------- KEYBOARD ----------------

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        if text in "0123456789.+-*/":
            self.on_input(text.replace("*", "×").replace("/", "÷"))

        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self.calculate()

        elif key == Qt.Key_Backspace:
            self.display.setText(self.display.text()[:-1])

        elif key in (Qt.Key_Delete, Qt.Key_Escape):
            self.clear()

        else:
            super().keyPressEvent(event)

    # ---------------- THEME ----------------

    def apply_theme(self):
        self.setStyleSheet(build_theme())

    # ---------------- ANIMATION ----------------

    def animate_button(self, btn):
        anim = QPropertyAnimation(btn, b"geometry")
        anim.setDuration(120)
        btn.enterEvent = lambda e, a=anim: a.start()


# ---------------- RUN --------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec())
