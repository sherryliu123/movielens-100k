
import mysql.connector
conn=mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor = conn.cursor()
rate=[]
sum=0

user_movies = []
for i in range(1,10440):
    sql = "select userId,movieId,rating from u_test where id =%d" % i  # 读取测试集原先打分值
    cursor.execute(sql)
    umr = cursor.fetchone()
    user_movies.append(umr)

for user_movie in user_movies:
    rate = user_movie[2]
    user = user_movie[0]
    movie = user_movie[1]
    sql = "select pred from u_pred2 where userId =%d and movieId=%d" % (user,movie)  # 读取测试集预测打分值
    cursor.execute(sql)
    pred = cursor.fetchone()
    sum = sum + abs(rate - float(pred[0]))

mae = sum/10439
print("通过高分检验：预测结果集与测试结果集的平均绝对误差为：%f" % mae)









