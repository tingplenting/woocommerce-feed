import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost',user='root',password='',db='your_wp_db',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor) 
cur = conn.cursor()
