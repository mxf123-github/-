import pymysql
host = 'localhost'
port = 3306
db = 'cheku'
user = 'root'
password = 'root'
# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


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
        
if __name__ == '__main__':
    print(select('A100'))