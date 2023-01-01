# import argparse
import psycopg2 as pg
# import matplotlib.pyplot as plt
import pandas as pd

import sys
# import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QLabel, QLineEdit, \
    QVBoxLayout, QTabWidget, QComboBox, QTableWidget, QTableWidgetItem, QDateEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import Updater

host = 'dbfinalproject.cy4pbwrkxxik.us-east-1.rds.amazonaws.com'
dbname = 'dbfinalproject'
username = 'postgres'
password = '00000000'


# ===== GUI ================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Crypto Final Project'
        self.setWindowTitle(self.title)
        self.resize(640, 480)
        self.tabs = TabsWidget()
        self.setCentralWidget(self.tabs)


class LoginWindow(QWidget):
    def __init__(self, parent, tabs):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(300, 120)
        self.layout = QGridLayout()
        self.p = parent
        self.t = tabs

        label_username = QLabel('Username')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setText(username)
        self.lineEdit_username.setPlaceholderText(
            f'default username : {username}')
        self.layout.addWidget(label_username, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('Password')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setText(password)
        self.lineEdit_password.setPlaceholderText(
            f'default password : {password}')
        self.layout.addWidget(label_password, 1, 0)
        self.layout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.button_login_click_event)
        self.layout.addWidget(button_login, 2, 0, 1, 2)

        # layout.setRowMinimumHeight(2, 75)
        self.setLayout(self.layout)

    def button_login_click_event(self):
        global PGC
        a = self.lineEdit_username.text()
        b = self.lineEdit_password.text()
        conn_str = f'host={host} dbname={dbname} user={a} password={b}'
        print(f'connecting to host {host}')
        PGC = PostgresConnectionClass(conn_str)
        print('database updating')
        u = Updater.Updater(PGC.conn, PGC.cursor)
        u.update()
        print(f'connected to host {host}')

        self.deleteLater()
        self.p.deleteLater()
        self.t.add_tabs()


class LoginTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.p = parent
        self.layout = QVBoxLayout(self)
        self.button_login = QPushButton("Login")
        self.login_window = LoginWindow(self, self.p)
        self.button_login.clicked.connect(self.button_login_click_event)
        # self.login_button.setFixedSize(100, 40)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.button_login)
        self.setLayout(self.layout)

    def button_login_click_event(self):
        self.login_window.show()


class ChartTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label_cname = QLabel('Currency')
        self.cb_cname = QComboBox()
        rows = PGC.getCryptoType()
        self.cb_cname.addItems(rows)
        self.layout.addWidget(self.label_cname, 0, 0)
        self.layout.addWidget(self.cb_cname, 0, 1)

        self.label_sdate = QLabel('Start Date')
        self.dateEdit_sdate = QDateEdit(calendarPopup=True)
        self.layout.addWidget(self.label_sdate, 1, 0)
        self.layout.addWidget(self.dateEdit_sdate, 1, 1, 1, 2)

        self.label_edate = QLabel('End Date')
        self.dateEdit_edate = QDateEdit(calendarPopup=True)
        self.layout.addWidget(self.label_edate, 2, 0)
        self.layout.addWidget(self.dateEdit_edate, 2, 1, 1, 2)

        self.button_query = QPushButton('Query')
        self.button_query.clicked.connect(self.button_query_click_event)
        self.layout.addWidget(self.button_query, 3, 0, 1, 3)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, 4, 0, 2, 3)

        # self.toolbar = NavigationToolbar2QT(self.canvas, self.canvas)

        # layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)

    def button_query_click_event(self):
        global PGC
        cname = self.cb_cname.currentText()

        xsdate = self.dateEdit_sdate.text()
        xedate = self.dateEdit_edate.text()
        sdate = ''
        edate = ''
        for s in xsdate:
            if s == '/':
                sdate += '-'
            else:
                sdate += s
        for e in xedate:
            if e == '/':
                edate += '-'
            else:
                edate += e

        # PGC.drawChart(cname, sdate, edate)
        # =======draw chart=======
        self.figure.clf()
        chart = self.figure.add_subplot(111)

        chart.clear()

        chartlist = PGC.getHistoricalData(cname, sdate, edate, 'date', 'ASC')
        df = pd.DataFrame(chartlist, columns=[
                          'name', 'date', 'close', 'open', 'high', 'low', 'vol', 'change'])
        df.set_index('date', inplace=True)
        df.drop(['name', 'vol', 'change'], axis=1, inplace=True)

        width = 0.6
        width2 = 0.1
        up = df[df.close >= df.open]
        down = df[df.close < df.open]
        col1 = 'green'
        col2 = 'red'

        chart.bar(up.index, up.close - up.open,
                  width, bottom=up.open, color=col1)
        chart.bar(up.index, up.high - up.close,
                  width2, bottom=up.close, color=col1)
        chart.bar(up.index, up.low - up.open,
                  width2, bottom=up.open, color=col1)

        chart.bar(down.index, down.close - down.open,
                  width, bottom=down.open, color=col2)
        chart.bar(down.index, down.high - down.open,
                  width2, bottom=down.open, color=col2)
        chart.bar(down.index, down.low - down.close,
                  width2, bottom=down.close, color=col2)
        chart.set_title(f"{cname} Price")
        chart.tick_params(axis='both', which='minor', labelsize=6)
        chart.tick_params(axis='both', which='major', labelsize=6)
        chart.set_xticks(chart.get_xticks(),
                         chart.get_xticklabels(), rotation=20, ha='right')

        self.canvas.draw()

        pass


class HistoricalTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label_cname = QLabel('Currency')
        self.cb_cname = QComboBox()
        cnames = PGC.getCryptoType()
        # print(f'Debug: {cnames}')
        self.cb_cname.addItems(cnames)
        self.layout.addWidget(self.label_cname, 0, 0)
        self.layout.addWidget(self.cb_cname, 0, 1)

        self.label_orders = QLabel('Sort By')
        self.cb_orders = QComboBox()
        self.orders = ['date', 'closing_price', 'opening_price',
                       'highest_price', 'lowest_price', 'volume', 'change']
        # print(f'Debug: {orders}')
        self.cb_orders.addItems(self.orders)
        self.cb_dirs = QComboBox()
        dirs = ['asc', 'desc']
        # print(f'Debug: {dirs}')
        self.cb_dirs.addItems(dirs)
        self.layout.addWidget(self.label_orders, 1, 0)
        self.layout.addWidget(self.cb_orders, 1, 1)
        self.layout.addWidget(self.cb_dirs, 1, 2)

        self.label_sdate = QLabel('Start Date')
        self.dateEdit_sdate = QDateEdit(calendarPopup=True)
        self.layout.addWidget(self.label_sdate, 2, 0)
        self.layout.addWidget(self.dateEdit_sdate, 2, 1, 1, 2)

        self.label_edate = QLabel('End Date')
        self.dateEdit_edate = QDateEdit(calendarPopup=True)
        self.layout.addWidget(self.label_edate, 3, 0)
        self.layout.addWidget(self.dateEdit_edate, 3, 1, 1, 2)

        self.button_query = QPushButton('Query')
        self.button_query.clicked.connect(self.button_query_click_event)
        self.layout.addWidget(self.button_query, 4, 0, 1, 3)

        self.table = QTableWidget()
        self.layout.addWidget(self.table, 5, 0, 1, 3)

        # layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)

    def button_query_click_event(self):
        global PGC
        cname = self.cb_cname.currentText()
        xsdate = self.dateEdit_sdate.text()
        xedate = self.dateEdit_edate.text()
        sdate = ''
        edate = ''
        for s in xsdate:
            if s == '/':
                sdate += '-'
            else:
                sdate += s
        for e in xedate:
            if e == '/':
                edate += '-'
            else:
                edate += e

        # print(f'{sdate} + {edate}')
        order = self.cb_orders.currentText()
        dir = self.cb_dirs.currentText()

        data = PGC.getHistoricalData(cname, sdate, edate, order, dir)
        self.table.clear()

        rlen = len(data)
        if rlen == 0:
            return
        clen = len(data[0])
        self.table.setRowCount(rlen)
        self.table.setColumnCount(clen - 1)
        self.table.setHorizontalHeaderLabels(self.orders)
        for r in range(rlen):
            for c in range(clen):
                if not c == 0:
                    self.table.setItem(
                        r, c - 1, QTableWidgetItem(str(data[r][c])))
                # print(data[r][c])


class TabsWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tab_login = LoginTab(self)

        # self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab_login, "Login Tab")
        # self.tabs.addTab(self.tab2, "Tab 2")

        self.layout.addWidget(self.tabs)
        # self.setLayout(self.layout)

    def add_tabs(self):
        tab_historical = HistoricalTab()
        tab_chart = ChartTab()
        self.tabs.addTab(tab_historical, "Historical Data")
        self.tabs.addTab(tab_chart, "Charts")


def gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


# ===== End GUI ==============================================================

class PostgresConnectionClass:
    def __init__(self, conn_str=''):
        self.conn = None
        if conn_str != '':
            self.conn = pg.connect(conn_str)
            self.cursor = self.conn.cursor()

    # Get all crypto 回傳所有貨幣種類
    def getCryptoType(self):
        if not self.conn:
            return []

        sql_query = 'SELECT DISTINCT type FROM cryptocurrency ORDER BY type'
        self.cursor.execute(sql_query)

        cnames = self.cursor.fetchall()
        cnames = [c[0] for c in cnames]
        return cnames

    #
    def askCryptoType(self):
        if not self.conn:
            return []
        print('select crypto type :')
        cnames = self.getCryptoType()
        i = 0
        for c in cnames:
            print(f'[{i}]{c}')
            i = i + 1
        cname = cnames[int(input())]
        return cname

    # Get Historical Data 回傳指定日期間歷史資料
    def getHistoricalData(self, cname, sdate, edate, order='None', dir='None'):
        if not self.conn:
            return []

        if order == 'None':
            sql_query = f"SELECT * FROM cryptocurrency WHERE type = '{cname}' AND (date between '{sdate}' and '{edate}')"
        else:
            sql_query = f"SELECT * FROM cryptocurrency WHERE type = '{cname}' AND (date between '{sdate}' and '{edate}') ORDER BY {order} {dir}"
        self.cursor.execute(sql_query)

        data = self.cursor.fetchall()
        return data

    # End Connection
    def endConnection(self):
        if not self.conn:
            return
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


PGC = PostgresConnectionClass()


# ==================================================================


def main():
    gui()


if __name__ == "__main__":
    main()
