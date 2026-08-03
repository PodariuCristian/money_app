import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QTableWidget, QTableWidgetItem,
    QTabWidget, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    CURRENT_YEAR = 2026
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financials")
        self.setGeometry(100, 100, 1100, 530)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.combo = QComboBox()
        main_layout.addWidget(self.combo)
        main_layout.addWidget(self.tab_widget, stretch=1)
        main_layout.addWidget(self.combo)

        # Update the label whenever the selection changes
        self.combo.currentTextChanged.connect(self.on_selection_changed)

        #create tab widget and set it to layout
        self.tab_widget = QTabWidget()
        self.initTab1()
        self.initTab2()
        self.initTab3()
        self.initTab4()

        main_layout.addWidget(self.tab_widget)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def on_selection_changed(self, text):
        self.CURRENT_YEAR = int(text)
        # Refresh your tabs
        self.refresh_tab1()
        self.refresh_tab2()
        self.refresh_tab3()
        self.refresh_tab4()

    def initTab1(self):
        self.tab1 = QWidget()
        layout = QVBoxLayout(self.tab1)
        self.tab_widget.addTab(self.tab1, "Stats Overview")

    def initTab2(self):
        self.tab2 = QTabWidget()
        self.tab_widget.addTab(self.tab2, "Income")

    def initTab3(self):
        self.tab3 = QTabWidget()
        self.tab_widget.addTab(self.tab3, "Fixed Costs")

    def initTab4(self):
            self.tab4 = QTabWidget()
            self.tab_widget.addTab(self.tab4, "Spendings")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())