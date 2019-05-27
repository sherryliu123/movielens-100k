import mysql.connector

conn = mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor = conn.cursor()
def avg():
    avg = 0
    for a in range(1, 944):  # 计算每个用户打分的平均值
        sum = 0
        j = 0
        i = 0
        b = 0
        sql = 'select rating from u_base where userId=%d ' % a
        cursor.execute(sql)
        ratings = cursor.fetchall()
        i = len(ratings)
        for j in range(i):
            sum = sum + ratings[j][0]
        b = sum / i
        avg = avg + b
        print("用户%d对电影的平均打分为：%f" % (a, b))
        # sql = "insert into avg(userId,avg) values (%d, %f)" % (a, float(b))
        # cursor.execute(sql)
        # conn.commit()
    return avg

avg1=avg()/943
print("用户对电影的平均打分为：%f" % avg1)
