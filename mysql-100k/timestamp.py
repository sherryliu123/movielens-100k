import mysql.connector

conn=mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor = conn.cursor()

conn1=mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor1 = conn1.cursor()

conn2=mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor2 = conn2.cursor()

conn3=mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor3 = conn3.cursor()

conn4=mysql.connector.connect(host="localhost",
                               user="root", password="960516",
                               db="movielens_100k", charset="utf8")  # conn为连接到的数据库
cursor4 = conn4.cursor()

#sum = 0
for i in range (1,944):
    sql='select count(*) from u_data where userId=%d '% i
    cursor.execute(sql)
    count=cursor.fetchone()
    num1 = int(0.9 * count[0])
    num2 = count[0] - int(0.9 * count[0])
    #sum +=count[0]
    #print(int(0.9*count[0]))
    sql = 'select userId,movieId,rating,timestamp from u_data where userId=%d order by timestamp desc  ' % i  # 按照userID升序提取出用户看过的电影movieId和评分rate
    cursor1.execute(sql)
    train = cursor1.fetchall()
    bases=[]
    for j in range(num1):
        bases.append(train[j])
    for base in bases:
        sql = "insert into u_base(userId,movieId,rating,timestamp) values (%d,%d,%d,%f)" % (base[0], base[1], base[2], base[3])
        cursor2.execute(sql)
        conn2.commit()
    sql = 'select userId,movieId,rating,timestamp from u_data where userId=%d order by timestamp asc  ' % i  # 按照userID升序提取出用户看过的电影movieId和评分rate
    cursor3.execute(sql)
    testset = cursor3.fetchall()
    tests = []
    for t in range(num2):
        tests.append(testset[t])
    for test in tests:
        sql = "insert into u_test(userId,movieId,rating,timestamp) values (%d,%d,%d,%f)" % (test[0], test[1], test[2], test[3])
        cursor4.execute(sql)
        conn4.commit()
    print(i)






