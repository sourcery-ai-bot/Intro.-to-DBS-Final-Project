import datetime
import validate
import web_crawler2
import psycopg2


class Updater:
    def __init__(self, conn, cursor):
        # self.connection = psycopg2.connect(
        #     f'host={host} dbname={dbname} user={username} password={password}')
        # self.cursor = self.connection.cursor()
        self.connection = conn
        self.cursor = cursor
        web_crawler2.OpenDriver()

    def getLastDate(self):
        sql_query = 'SELECT MAX(date) FROM cryptocurrency'
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()[0][0]

    def update(self):
        self.lastDate = self.getLastDate()
        # if datetime.date.today() > self.lastDate:
        #     new_data = web_crawler2.crawl()
        #     if datetime.datetime.strptime(new_data[0][1], "%b %d, %Y").date() > self.lastDate:
        #         for i in new_data:
        #             record = validate.validate(i)
        #             sql_query = f'INSERT INTO cryptocurrency VALUES ({record})'
        #             self.cursor.execute(sql_query)
        #         self.connection.commit()

        if datetime.date.today() <= self.lastDate:
            # print('database is already updated')
            web_crawler2.CloseDriver()
            return

        new_data = web_crawler2.crawl_first()
        if datetime.datetime.strptime(new_data[0][1], "%b %d, %Y").date() == self.lastDate:
            # print('database is already updated')
            web_crawler2.CloseDriver()
            return

        new_data = web_crawler2.crawl()
        for i in new_data:
            record = validate.validate(i)
            sql_query = f'INSERT INTO cryptocurrency VALUES ({record})'
            self.cursor.execute(sql_query)
        self.connection.commit()
        web_crawler2.CloseDriver()
