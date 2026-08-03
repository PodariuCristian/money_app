import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QTabWidget, QComboBox,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries,
    QBarSeries, QBarSet, QBarCategoryAxis,
    QValueAxis,
)
from PySide6.QtGui import QPainter
from datetime import datetime

class MainWindow(QMainWindow):
    CURRENT_YEAR = 2026
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoneyApp")
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
        self.tab_widget.addTab(self.tab1, "Stats Overview")

        # Main layout for the tab
        layout = QHBoxLayout(self.tab1)

        # -------------------- Monthly Summary --------------------
        self.monthly_group = QGroupBox("Monthly Summary")
        monthly_layout = QVBoxLayout(self.monthly_group)

        # ---------------- Month selection ----------------
        self.month_combo = QComboBox()

        months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(datetime.now().month - 1)

        monthly_layout.addWidget(self.month_combo)

        # ---------------- Income / Outcome row ----------------
        income_layout = QHBoxLayout()

        # ---------------- Income Label ----------------
        income_layout.addWidget(QLabel("Income:"))

        self.income_edit = QLineEdit()
        self.income_edit.setPlaceholderText("0.00")
        self.income_edit.setReadOnly(True)
        income_layout.addWidget(self.income_edit)

        # ---------------- Outcome Label ----------------
        income_layout.addWidget(QLabel("Outcome:"))

        self.outcome_edit = QLineEdit()
        self.outcome_edit.setPlaceholderText("0.00")
        income_layout.addWidget(self.outcome_edit)
        self.outcome_edit.setReadOnly(True)

        monthly_layout.addLayout(income_layout)

        # ---------------- Percentage / Previous Month row ----------------
        stats_layout = QHBoxLayout()

        # ---------------- Income vs Outcome percentage ----------------
        stats_layout.addWidget(QLabel("Income/Outcome:"))

        self.percent_edit = QLineEdit()
        self.percent_edit.setReadOnly(True)
        self.percent_edit.setPlaceholderText("0.00 %")
        stats_layout.addWidget(self.percent_edit)

        # ---------------- Difference from previous month ----------------
        stats_layout.addWidget(QLabel("Previous Month:"))

        self.previous_diff_edit = QLineEdit()
        self.previous_diff_edit.setReadOnly(True)
        self.previous_diff_edit.setPlaceholderText("0.00")
        stats_layout.addWidget(self.previous_diff_edit)

        monthly_layout.addLayout(stats_layout)

        # ---------------- Pie Chart ----------------
        self.monthly_series = QPieSeries()
        self.monthly_series.clear()

        self.monthly_series.append("Food", 450)
        self.monthly_series.append("Rent", 1200)
        self.monthly_series.append("Transport", 180)
        self.monthly_series.append("Entertainment", 220)

        self.monthly_chart = QChart()
        self.monthly_chart.addSeries(self.monthly_series)
        self.monthly_chart.setTitle("Monthly Spending")
        self.monthly_chart.legend().setVisible(True)

        self.monthly_chart_view = QChartView(self.monthly_chart)
        self.monthly_chart_view.setRenderHint(QPainter.Antialiasing)

        monthly_layout.addWidget(self.monthly_chart_view, stretch=1)

        # ---------------- Empty Bar Chart ----------------

        self.bar_set = QBarSet("Expenses")

        self.bar_series = QBarSeries()
        self.bar_series.append(self.bar_set)

        self.bar_chart = QChart()
        self.bar_chart.addSeries(self.bar_series)
        self.bar_chart.setTitle("Monthly Expenses by Category")

        # Categories (x-axis)
        self.categories = [
            "Food",
            "Rent",
            "Transport",
            "Utilities",
            "Entertainment",
            "Other"
        ]

        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)

        # Amount axis (y-axis)
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Amount")
        self.axis_y.setRange(0, 100)

        self.bar_chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.bar_chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.bar_series.attachAxis(self.axis_x)
        self.bar_series.attachAxis(self.axis_y)

        self.bar_chart_view = QChartView(self.bar_chart)
        self.bar_chart_view.setRenderHint(QPainter.Antialiasing)

        monthly_layout.addWidget(self.bar_chart_view, stretch=1)

        # -------------------- Yearly Summary --------------------
        self.yearly_group = QGroupBox("Yearly Summary")
        yearly_layout = QVBoxLayout(self.yearly_group)

        # Split the window evenly
        layout.addWidget(self.monthly_group, 1)
        layout.addWidget(self.yearly_group, 1)

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