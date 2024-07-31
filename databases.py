import pymysql
import datetime as dt
def connect_db(): #pymysql 사용해서 DB연결
    global connect , cursor
    connect = pymysql.connect(host='localhost',
                              user='root',
                              passwd='1234',
                              db='CCM_CINEMA',
                              charset='utf8');

    cursor = connect.cursor()

connect_db()





