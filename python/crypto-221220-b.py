import argparse
import psycopg2 as pg
import matplotlib

import sys
# import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QLabel, QLineEdit, \
    QVBoxLayout, QTabWidget, QComboBox, QTableWidget, QTableWidgetItem

parser = argparse.ArgumentParser()
app_type = parser.add_mutually_exclusive_group()
app_type.add_argument('-cmd', dest='cmd',
                      action='store_true', help='[REQUIRED] NO GUI')
app_type.add_argument('-gui', dest='gui',
                      action='store_true', help='[REQUIRED] GUI')

# parser.add_argument('-host', type=str, help='server name')
# parser.add_argument('-db', type=str, help='db name')
default_username = 'lstrings'
default_password = '8454'
parser.add_argument('-u', type=str, dest='username',
                    help='admin username', default=default_username)
parser.add_argument('-p', type=str, dest='password',
                    help='admin password', default=default_password)

# parser.print_help()

args = parser.parse_args()

if not args.cmd and not args.gui:
    print('error: one of the arguments "-cmd" "-gui" is required\n')
    parser.print_help()

host = '127.0.0.1'
dbname = 'covid19'
username = args.username
password = args.password


# cursor = pg._psycopg.cursor()


# print(f'{host},  {dbname},  {username},  {password}')


def cmd():
    global PGC

    conn_str = f'host={host} dbname={dbname} user={username} password={password}'
    print(f'connecting to host {host}')
    # conn = pg.connect(conn_str)
    PGC = PostgresConnectionClass(conn_str)
    print(f'connected to host {host}')
    # cursor = conn.cursor()

    query = ''
    while query != '3':
        query = input(
            '\n\nActions:\n[1] Historical Data\n[2] Chart\n[3] Exit\n')
        if query == '1':
            # c_name = askCryptoType()
            c_name = PGC.askCryptoType()
            s_date = input('enter start date YYYY-MM-DD :\t')
            e_date = input('enter end date YYYY-MM-DD :\t')

            # cursor.execute("SELECT * FROM public.containment ORDER BY date ASC, country_code ASC LIMIT 100")
            # rows = getHistoricalData(c_name, s_date, e_date)
            data = PGC.getHistoricalData(c_name, s_date, e_date)
            for row in data:
                for attr in row:
                    print(f'{attr}\t', end='')
                print()
        elif query == '2':
            # c_name = askCryptoType()
            c_name = PGC.askCryptoType()
            s_date = input('enter start date YYYY-MM-DD :\t')
            e_date = input('enter end date YYYY-MM-DD :\t')

            # drawChart(c_name, s_date, e_date)
            PGC.drawChart(c_name, s_date, e_date)

    # conn.commit()
    # cursor.close()
    # conn.close()
    PGC.endConnection()


# ===== GUI ================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Crypto Final Project'
        self.setWindowTitle(self.title)
        self.setFixedSize(640, 480)
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
        # conn = pg.connect(conn_str)
        PGC = PostgresConnectionClass(conn_str)
        print(f'connected to host {host}')
        # cursor = conn.cursor()

        # msg = QMessageBox()
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

        self.cb_cname = QComboBox()
        rows = PGC.getCryptoType()
        self.cb_cname.addItems(rows)
        self.layout.addWidget(self.cb_cname, 0, 0)

        self.label_sdate = QLabel('Start Date')
        self.lineEdit_sdate = QLineEdit()
        self.lineEdit_sdate.setPlaceholderText('2000-01-01 Start Date')
        self.layout.addWidget(self.label_sdate, 1, 0)
        self.layout.addWidget(self.lineEdit_sdate, 1, 1)

        self.label_edate = QLabel('End Date')
        self.lineEdit_edate = QLineEdit()
        self.lineEdit_edate.setPlaceholderText('2000-01-01 End Date')
        self.layout.addWidget(self.label_edate, 2, 0)
        self.layout.addWidget(self.lineEdit_edate, 2, 1)

        self.button_query = QPushButton('Query')
        self.button_query.clicked.connect(self.button_query_click_event)
        self.layout.addWidget(self.button_query, 3, 0)

        # layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)

    def button_query_click_event(self):
        global PGC
        cname = self.cb_cname.currentText()
        sdate = self.lineEdit_sdate.text()
        edate = self.lineEdit_edate.text()

        PGC.drawChart(cname, sdate, edate)
        pass


class HistoricalTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cb_cname = QComboBox()
        cnames = PGC.getCryptoType()
        print(f'a: {cnames}')
        self.cb_cname.addItems(cnames)
        self.layout.addWidget(self.cb_cname, 0, 0)

        self.label_sdate = QLabel('Start Date')
        self.lineEdit_sdate = QLineEdit()
        self.lineEdit_sdate.setPlaceholderText('2000-01-01 Start Date')
        self.layout.addWidget(self.label_sdate, 1, 0)
        self.layout.addWidget(self.lineEdit_sdate, 1, 1)

        self.label_edate = QLabel('End Date')
        self.lineEdit_edate = QLineEdit()
        self.lineEdit_edate.setPlaceholderText('2000-01-01 End Date')
        self.layout.addWidget(self.label_edate, 2, 0)
        self.layout.addWidget(self.lineEdit_edate, 2, 1)

        self.button_query = QPushButton('Query')
        self.button_query.clicked.connect(self.button_query_click_event)
        self.layout.addWidget(self.button_query, 3, 0)

        self.table = QTableWidget()
        self.layout.addWidget(self.table, 4, 0, 1, 2)

        # layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)

    def button_query_click_event(self):
        global PGC
        cname = self.cb_cname.currentText()
        sdate = self.lineEdit_sdate.text()
        edate = self.lineEdit_edate.text()

        data = PGC.getHistoricalData(cname, sdate, edate)
        self.table.clear()

        rlen = len(data)
        if rlen == 0:
            return
        clen = len(data[0])
        self.table.setRowCount(rlen)
        self.table.setColumnCount(clen)
        for r in range(rlen):
            for c in range(clen):
                self.table.setItem(r, c, QTableWidgetItem(data[r][c]))
                print(data[r][c])


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


# ===== GUI =================================================================

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

        # == Need Implementation ===========================================
        sql_query = 'SELECT DISTINCT type FROM cryptocurrency ORDER BY type'
        # raise NotImplementedError

        self.cursor.execute(sql_query)
        # ==================================================================

        # self.cursor.execute("SELECT continent_name FROM continent LIMIT 100")
        cnames = self.cursor.fetchall()
        # cnames = [['Bitcoin'], ['Ethereum'], ['Tether'], ['Binance Coin']]  # Test Data
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
    def getHistoricalData(self, cname, sdate, edate):
        if not self.conn:
            return []

        # == Need Implementation ===========================================

        # 我如何知道依哪一行排序 ?
        # 還是現在這個 function 沒有依任意行排序的功能 ?
        sql_query = f'SELECT * FROM cryptocurrency WHERE date between {sdate} and {edate}'
        # sql_query = f'SELECT * FROM cryptocurrency WHERE date between {sdate} and {edate} ORDER BY {column}'

        # raise NotImplementedError

        self.cursor.execute(sql_query)
        # ==================================================================

        # self.cursor.execute("SELECT * FROM public.containment ORDER BY date ASC, country_code ASC LIMIT 100")
        data = self.cursor.fetchall()
        # data = [['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc'],
        #         ['3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234', 'abc', '3234', '12341234',
        #          'abc']]  # Test Data
        return data

    # Draw Chart
    def drawChart(self, cname, sdate, edate):
        if not self.conn:
            return
        # == Need Implementation ===========================================
        raise NotImplementedError

        # ==================================================================

    # End Connection
    def endConnection(self):
        if not self.conn:
            return
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


PGC = PostgresConnectionClass()


def main():
    if args.cmd:
        cmd()
    elif args.gui:
        gui()


if __name__ == "__main__":
    main()
