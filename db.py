import pymysql
import time  
import datetime
host = 'localhost'
port = 3306
db = 'cheku'
user = 'root'
password = 'root'
# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn

#检测db是否存在此车牌
def select(licenseNum_detected):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("select time from license where licenseNum=('%s') limit 1" % (licenseNum_detected))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if results: 
        mysql_datetime=results[0].get('time')
        current_time = datetime.datetime.now()
        # print(mysql_datetime,current_time)
        if mysql_datetime < current_time:
            return 'expired'
        elif mysql_datetime >= current_time:
            return 'ok'
    return 'not sign'

    
if __name__ == '__main__':
    print(select('A100'))