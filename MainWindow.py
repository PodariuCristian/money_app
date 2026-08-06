import sys
import Constants
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries,
    QBarSeries, QBarSet, QBarCategoryAxis,
    QValueAxis
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTabWidget,
    QComboBox, QGroupBox, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from database.schema import create_tables
from database.seed import seed_categories
from database import queries

from PySide6.QtWidgets import QTableWidgetItem

class MainWindow(QMainWindow):
    CURRENT_YEAR = datetime.now().year

    def __init__(self):
        super().__init__()
        create_tables()
        seed_categories()
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
        self.build_income_tab()
        self.load_table(self.income_table, "Income", total_row=3)

        self.build_fix_costs_tab()
        self.load_table(self.fixed_table, "Fixed")
        self.load_table(self.utilities_table, "Utility")
        self.load_table(self.subscriptions_table, "Subscription")

        self.build_spendings_tab()
        self.load_table(self.spendings_table, "Expense")

        self.tabs.addTab(QWidget(), "Statistics")

    # -------------------- Define Tab in Main Window --------------------
    def build_overview_tab(self, title, is_monthly = True):
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
            half.addWidget(self.build_overview_tab("Monthly Summary",True),1)
            half.addWidget(self.build_overview_tab("Yearly Summary",False),1)

    def build_income_tab(self):
        # ---------- Create Income tab ----------
        self.income_tab = QWidget()
        self.tabs.addTab(self.income_tab, "Income")

        # ---------- Create Income table ----------
        income_layout = QVBoxLayout(self.income_tab)
        self.income_table = QTableWidget(4, 12)

        self.income_table.setHorizontalHeaderLabels(Constants.months)
        self.income_table.setVerticalHeaderLabels(Constants.income_header)

        # Make the table fill the available space
        header = self.income_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        income_layout.addWidget(self.income_table, 1)
        self.income_table.cellChanged.connect(lambda row, col: self.save_table(self.income_table, "Income", row, col, total_row=3))

        # ---------- Income Bar Chart ----------
        self.income_bar_set = QBarSet("Income")

        # Empty values for the 12 months
        self.income_bar_set.append([500] * 12)

        self.income_bar_series = QBarSeries()
        self.income_bar_series.append(self.income_bar_set)

        self.income_chart = QChart()
        self.income_chart.addSeries(self.income_bar_series)
        self.income_chart.setTitle("Income by Month")

        self.income_axis_x = QBarCategoryAxis()
        self.income_axis_x.append(Constants.months)

        self.income_axis_y = QValueAxis()
        self.income_axis_y.setTitleText("Income")
        self.income_axis_y.setRange(0, 10000)

        self.income_chart.addAxis(self.income_axis_x, Qt.AlignBottom)
        self.income_chart.addAxis(self.income_axis_y, Qt.AlignLeft)

        self.income_bar_series.attachAxis(self.income_axis_x)
        self.income_bar_series.attachAxis(self.income_axis_y)

        self.income_chart_view = QChartView(self.income_chart)
        self.income_chart_view.setRenderHint(QPainter.Antialiasing)

        income_layout.addWidget(self.income_chart_view, 4)

    def build_fix_costs_tab(self):
        # ---------- Create Fix Costs tab ----------
        self.fix_costs_page = QWidget()
        self.tabs.addTab(self.fix_costs_page, "Fix Spendings")

        layout = QVBoxLayout(self.fix_costs_page)

        # ---------- Create Fix Costs table ----------
        self.fixed_table = QTableWidget(5, 12)
        self.fixed_table.setHorizontalHeaderLabels(Constants.months)
        self.fixed_table.setVerticalHeaderLabels(Constants.fix_spendings)
        self.fixed_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.fixed_table, 3)
        self.fixed_table.cellChanged.connect(lambda row, col: self.save_table(self.fixed_table, "Fixed", row, col))

        # ---------- Create Utilities table ----------
        self.utilities_table = QTableWidget(5, 12)
        self.utilities_table.setHorizontalHeaderLabels(Constants.months)
        self.utilities_table.setVerticalHeaderLabels(Constants.utilities)
        self.utilities_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.utilities_table, 3)
        self.utilities_table.cellChanged.connect(lambda row, col: self.save_table(self.utilities_table, "Utility", row, col))

        # ---------- Create Subscriptions table ----------
        self.subscriptions_table = QTableWidget(2, 12)
        self.subscriptions_table.setHorizontalHeaderLabels(Constants.months)
        self.subscriptions_table.setVerticalHeaderLabels(Constants.subscriptions)
        self.subscriptions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.subscriptions_table, 2)
        self.subscriptions_table.cellChanged.connect(lambda row, col: self.save_table(self.subscriptions_table, "Subscription", row, col))

    def build_spendings_tab(self):
        # ---------- Create Fix Costs tab ----------
        self.spendings_tab = QWidget()
        self.tabs.addTab(self.spendings_tab, "Spendings")
        
        # ---------- Create Spendings table ----------
        spendings_layout = QVBoxLayout(self.spendings_tab)
        self.spendings_table = QTableWidget(16, 12)
        
        self.spendings_table.setHorizontalHeaderLabels(Constants.months)
        self.spendings_table.setVerticalHeaderLabels(Constants.categories)
        
        # Make the table fill the available space
        header = self.spendings_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        spendings_layout.addWidget(self.spendings_table, 3)
        self.spendings_table.cellChanged.connect(lambda row, col: self.save_table(self.spendings_table, "Expense", row, col))

        # ---------- Spendings Bar Chart ----------
        self.spendings_bar_set = QBarSet("Income")

        # Empty values for the 12 months
        self.spendings_bar_set.append([7500] * 16)

        self.spendings_bar_series = QBarSeries()
        self.spendings_bar_series.append(self.spendings_bar_set)

        self.spendings_chart = QChart()
        self.spendings_chart.addSeries(self.spendings_bar_series)
        self.spendings_chart.setTitle("Spendings by Categorie")

        self.income_axis_x = QBarCategoryAxis()
        self.income_axis_x.append(Constants.categories)

        self.income_axis_y = QValueAxis()
        self.income_axis_y.setTitleText("Income")
        self.income_axis_y.setRange(0, 10000)

        self.spendings_chart.addAxis(self.income_axis_x, Qt.AlignBottom)
        self.spendings_chart.addAxis(self.income_axis_y, Qt.AlignLeft)

        self.spendings_bar_series.attachAxis(self.income_axis_x)
        self.spendings_bar_series.attachAxis(self.income_axis_y)

        self.spendings_chart_view = QChartView(self.spendings_chart)
        self.spendings_chart_view.setRenderHint(QPainter.Antialiasing)

        spendings_layout.addWidget(self.spendings_chart_view, 2)

    def load_table(self, table_widget, section, total_row=None):
        """
        Loads data from the database into any monthly table.
        Parameters
        ----------
        table_widget : QTableWidget
            The table to populate.
        category_type : str
            "Income", "Expense", "Fixed", "Utility", "Subscription"
        total_row : int | None
            Row index that should display totals.
            Pass None if the table has no total row.
        """
        year = int(self.comboBox.currentText())
        data = queries.load_monthly_values(year,  section)
        table_widget.blockSignals(True)
        table_widget.clearContents()
        rows = table_widget.rowCount()
        cols = table_widget.columnCount()
        # Populate the table
        for row in range(rows):
            # Skip the total row
            if total_row is not None and row == total_row:
                continue
            category = table_widget.verticalHeaderItem(row).text()
            if category not in data:
                continue
            for month, amount in data[category].items():
                table_widget.setItem(
                    row, month - 1, QTableWidgetItem(f"{amount:.2f}")
                )

        # Calculate totals if requested
        if total_row is not None:
            for col in range(cols):
                total = 0.0
                for row in range(rows):
                    if row == total_row:
                        continue
                    item = table_widget.item(row, col)
                    if item is None:
                        continue
                    try:
                        total += float(item.text())
                    except ValueError:
                        pass
                table_widget.setItem(
                    total_row, col, QTableWidgetItem(f"{total:.2f}")
                )
        table_widget.blockSignals(False)

    def save_table(self, table_widget, section, row, column, total_row=None):
        
        """
        Saves an edited cell to the database and updates the total row.
        Parameters
        ----------
        table_widget : QTableWidget
        row : int
        column : int
        total_row : int | None
            Row containing totals. Pass None if the table has no total row.
        """
        # Ignore edits to the total row
        if total_row is not None and row == total_row:
            return
        item = table_widget.item(row, column)
        if item is None:
            return
        text = item.text().strip()
        # Empty cell = zero
        if text == "":
            amount = 0.0
        else:
            try:
                amount = float(text)
            except ValueError:
                # Invalid input: restore to zero
                table_widget.blockSignals(True)
                item.setText("0.00")
                table_widget.blockSignals(False)
                return

        # Category name comes from the row header
        category = table_widget.verticalHeaderItem(row).text()

        # Current year
        year = int(self.comboBox.currentText())

        # January = column 0
        month = column + 1
        # Save to SQLite
        queries.save_monthly_value(
            section=section,
            category=category,
            year=year,
            month=month,
            amount=amount
        )

        # Update total row if the table has one
        if total_row is not None:
            total = 0.0
            for r in range(table_widget.rowCount()):
                if r == total_row:
                    continue
                cell = table_widget.item(r, column)
                if cell is None:
                    continue
                try:
                    total += float(cell.text())
                except ValueError:
                    pass
            table_widget.blockSignals(True)
            table_widget.setItem(
                total_row,
                column,
                QTableWidgetItem(f"{total:.2f}")
            )
            table_widget.blockSignals(False)
        # Optional: refresh charts
        if hasattr(self, "update_charts"):
            self.update_charts()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())