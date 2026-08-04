import sys
import Constants
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart,QChartView,QPieSeries,QBarSeries,QBarSet,QBarCategoryAxis,QValueAxis
)
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QTabWidget,
    QComboBox,QGroupBox,QLabel,QLineEdit
)

class MainWindow(QMainWindow):
    CURRENT_YEAR = datetime.now().year

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoneyApp")
        self.resize(1800, 950)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget();
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # -------------------- Year selection dropdown --------------------
        self.comboBox = QComboBox()
        years = [str(y) for y in range(self.CURRENT_YEAR - 2, self.CURRENT_YEAR + 5)]
        self.comboBox.addItems(years)
        self.comboBox.setCurrentText(str(self.CURRENT_YEAR))
        main_layout.addWidget(self.comboBox)

        # -------------------- Main tab widget --------------------
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 1)
        self.init_stats()

        # -------------------- Create other tabs --------------------
        for name in ("Income","Fixed Costs","Spendings"):
            self.tabs.addTab(QWidget(),name)

    # -------------------- Define Tab in Main Window --------------------
    def build_summary(self, title, is_monthly=True):
        groupBox = QGroupBox(title)
        boxLayout = QVBoxLayout(groupBox)

        # ---------------- Month/Year selection ----------------
        periodSelection = QComboBox()
        if is_monthly:
            periodSelection.addItems(Constants.months)
            periodSelection.setCurrentIndex(datetime.now().month-1)
        else:
            years=[str(y) for y in range(self.CURRENT_YEAR - 2,self.CURRENT_YEAR + 5)]
            periodSelection.addItems(years)
            periodSelection.setCurrentText(str(self.CURRENT_YEAR))
        boxLayout.addWidget(periodSelection)

        # ---------------- Income/Outcome Label ----------------
        row1=QHBoxLayout()
        income = QLineEdit()
        outcome = QLineEdit()
        income.setReadOnly(True)
        income.setPlaceholderText("0.00")
        outcome.setReadOnly(True)
        outcome.setPlaceholderText("0.00")
        row1.addWidget(QLabel("Income:"))
        row1.addWidget(income)
        row1.addWidget(QLabel("Outcome:"))
        row1.addWidget(outcome)
        boxLayout.addLayout(row1)

        # ---------------- Percentage / Previous Month row ----------------
        row2 = QHBoxLayout()
        percentage = QLineEdit()
        prevMonth = QLineEdit()
        percentage.setReadOnly(True)
        percentage.setPlaceholderText("0.00 %")
        prevMonth.setReadOnly(True)
        prevMonth.setPlaceholderText("0.00")
        row2.addWidget(QLabel("Income/Outcome:"))
        row2.addWidget(percentage)
        row2.addWidget(QLabel("Previous Month:" if is_monthly else "Previous Year:"))
        row2.addWidget(prevMonth)
        boxLayout.addLayout(row2)

        # ---------------- Charts ----------------
        charts = QVBoxLayout()

        # ---------------- Pie Charts ----------------
        pie_series = QPieSeries()
        for i in Constants.categories:
            pie_series.append(i, 450)

        pie_chart = QChart()
        pie_chart.addSeries(pie_series)
        pie_chart.setTitle("Spending Distribution")
        pie_chart.legend().setVisible(True)
        pie_view = QChartView(pie_chart)
        pie_view.setRenderHint(QPainter.Antialiasing)

        # ---------------- Empty Bar Chart ----------------
        bar_set = QBarSet("Expenses")
        bar_series = QBarSeries()
        bar_series.append(bar_set)

        bar_chart = QChart()
        bar_chart.addSeries(bar_series)
        bar_chart.setTitle("Expenses by Category")

        axis_x = QBarCategoryAxis()
        axis_x.append(Constants.categories)
        axis_y = QValueAxis()
        axis_y.setRange(0,1000)
        bar_chart.addAxis(axis_x,Qt.AlignBottom)
        bar_chart.addAxis(axis_y,Qt.AlignLeft)
        bar_series.attachAxis(axis_x)
        bar_series.attachAxis(axis_y)
        bar_view = QChartView(bar_chart)
        bar_view.setRenderHint(QPainter.Antialiasing)

        charts.addWidget(pie_view, 3)
        charts.addWidget(bar_view, 2)
        boxLayout.addLayout(charts, 1)
        return groupBox

    def init_stats(self):
        tab = QWidget()
        self.tabs.addTab(tab,"Stats Overview")
        half = QHBoxLayout(tab)
        half.addWidget(self.build_summary("Monthly Summary",True),1)
        half.addWidget(self.build_summary("Yearly Summary",False),1)

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())