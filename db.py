import pymysql
import time  
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
        return True 
    return False

#插入日志数据：方向，车牌，是否缴费
def insert_log(direction,licenseNum_detected):
    conn=get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sqltime=time.strftime('%Y-%m-%d %H:%M:%S')
    param=(licenseNum_detected,sqltime)
    if(direction=='enter'):
        sql=str('insert into enter_cheku_log values(%s,%s,%s)')
    if(direction=='leave'):
        sql=str('insert into leave_cheku_log values(%s,%s,%s)')
    cursor.execute(sql,param)
    conn.commit()
    cursor.close()
    conn.close()
    
if __name__ == '__main__':
    print(select('A100'))
    print(insert_log('leave','123456',0))