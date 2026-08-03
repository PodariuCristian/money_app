
import sys
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
        self.setWindowTitle("Financial Dashboard")
        self.resize(1200,700)
        self._setup_ui()

    def _setup_ui(self):
        cw=QWidget(); self.setCentralWidget(cw)
        main=QVBoxLayout(cw)

        self.combo=QComboBox()
        years=[str(y) for y in range(self.CURRENT_YEAR-2,self.CURRENT_YEAR+3)]
        self.combo.addItems(years)
        self.combo.setCurrentText(str(self.CURRENT_YEAR))
        main.addWidget(self.combo)

        self.tabs=QTabWidget()
        main.addWidget(self.tabs,1)

        self.init_stats()
        for name in ("Income","Fixed Costs","Spendings"):
            self.tabs.addTab(QWidget(),name)

    def build_summary(self,title,is_monthly=True):
        box=QGroupBox(title)
        lay=QVBoxLayout(box)

        sel=QComboBox()
        if is_monthly:
            months=["January","February","March","April","May","June","July","August","September","October","November","December"]
            sel.addItems(months)
            sel.setCurrentIndex(datetime.now().month-1)
        else:
            years=[str(y) for y in range(self.CURRENT_YEAR-2,self.CURRENT_YEAR+3)]
            sel.addItems(years)
            sel.setCurrentText(str(self.CURRENT_YEAR))
        lay.addWidget(sel)

        r1=QHBoxLayout()
        inc=QLineEdit(); out=QLineEdit()
        inc.setReadOnly(True); out.setReadOnly(True)
        r1.addWidget(QLabel("Income:")); r1.addWidget(inc)
        r1.addWidget(QLabel("Outcome:")); r1.addWidget(out)
        lay.addLayout(r1)

        r2=QHBoxLayout()
        pct=QLineEdit(); diff=QLineEdit()
        pct.setReadOnly(True); diff.setReadOnly(True)
        r2.addWidget(QLabel("Income/Outcome:")); r2.addWidget(pct)
        r2.addWidget(QLabel("Previous Month:" if is_monthly else "Previous Year:")); r2.addWidget(diff)
        lay.addLayout(r2)

        charts=QHBoxLayout()

        pie_series=QPieSeries()
        pie_chart=QChart(); pie_chart.addSeries(pie_series); pie_chart.setTitle("Spending Distribution")
        pie_view=QChartView(pie_chart); pie_view.setRenderHint(QPainter.Antialiasing)

        bar_set=QBarSet("Expenses")
        bar_series=QBarSeries(); bar_series.append(bar_set)
        bar_chart=QChart(); bar_chart.addSeries(bar_series); bar_chart.setTitle("Expenses by Category")
        cats=["Food","Rent","Transport","Utilities","Entertainment","Other"]
        ax=QBarCategoryAxis(); ax.append(cats)
        ay=QValueAxis(); ay.setRange(0,100)
        bar_chart.addAxis(ax,Qt.AlignBottom); bar_chart.addAxis(ay,Qt.AlignLeft)
        bar_series.attachAxis(ax); bar_series.attachAxis(ay)
        bar_view=QChartView(bar_chart); bar_view.setRenderHint(QPainter.Antialiasing)

        charts.addWidget(pie_view,1)
        charts.addWidget(bar_view,1)
        lay.addLayout(charts,1)
        return box

    def init_stats(self):
        tab=QWidget()
        self.tabs.addTab(tab,"Stats Overview")
        hl=QHBoxLayout(tab)
        hl.addWidget(self.build_summary("Monthly Summary",True),1)
        hl.addWidget(self.build_summary("Yearly Summary",False),1)

if __name__=="__main__":
    app=QApplication(sys.argv)
    w=MainWindow()
    w.show()
    sys.exit(app.exec())