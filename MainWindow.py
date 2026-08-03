import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QTabWidget, QComboBox,
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    CURRENT_YEAR = 2026
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financials")
        self.resize(1100, 530)      # Initial window size
        self.setMinimumSize(800, 400)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Year selection dropdown
        self.combo = QComboBox()
        self.combo.addItems(["2025", "2026", "2027", "2028"])
        self.combo.setCurrentText(str(self.CURRENT_YEAR))
        self.combo.currentTextChanged.connect(self.on_selection_changed)

        # Prevent the combo box from stretching vertically
        self.combo.setMaximumHeight(30)
        main_layout.addWidget(self.combo)

        # Main tab widget
        self.tab_widget = QTabWidget()
        self.initTab1()
        self.initTab2()
        self.initTab3()
        self.initTab4()

        # Give the tab widget all remaining space
        main_layout.addWidget(self.tab_widget, stretch=1)

    def on_selection_changed(self, text):
        self.CURRENT_YEAR = int(text)
        print(f"Current year: {self.CURRENT_YEAR}")
        # Refresh your tabs here if needed
        # self.refresh_tab1()
        # self.refresh_tab2()
        # self.refresh_tab3()
        # self.refresh_tab4()

    def initTab1(self):
        self.tab1 = QWidget()
        layout = QVBoxLayout(self.tab1)
        self.tab_widget.addTab(self.tab1, "Stats Overview")

    def initTab2(self):
        self.tab2 = QWidget()
        layout = QVBoxLayout(self.tab2)
        self.tab_widget.addTab(self.tab2, "Income")

    def initTab3(self):
        self.tab3 = QWidget()
        layout = QVBoxLayout(self.tab3)
        self.tab_widget.addTab(self.tab3, "Fixed Costs")

    def initTab4(self):
        self.tab4 = QWidget()
        layout = QVBoxLayout(self.tab4)
        self.tab_widget.addTab(self.tab4, "Spendings")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())