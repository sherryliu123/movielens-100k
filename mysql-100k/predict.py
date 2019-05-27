import mysql.connector
import threading



def avg(a):    #提取a用户打分的平均值
    conn = mysql.connector.connect(host="localhost",
                                   user="root", password="960516",
                                   db="movielens_100k", charset="utf8")  # conn为连接到的数据库
    cursor = conn.cursor()

    sql = 'select avg from avg where userid = %d ' % a
    cursor.execute(sql)
    average = cursor.fetchall()
    return average[0][0]


def pred(u, movies):
    conn = mysql.connector.connect(host="localhost",
                                   user="root", password="960516",
                                   db="movielens_100k", charset="utf8")  # conn为连接到的数据库
    cursor = conn.cursor()

    #提取user1为u或者user2为u的用户与其他用户之间的pearson系数,其中要求两用户之间的pearson>0且共同看过5部以上电影
    sql = "select * from pearson2 where (user1=%d or user2=%d) and count>=5 and pearson>0  order by pearson desc" % (u, u)
    cursor.execute(sql)
    pearsons = cursor.fetchall()
    #print(pearsons)
    susers = []
    for pearson in pearsons:
        #print(pearson)
        #  user1 user2 pearson count
        if int(pearson[1]) == int(u):   #如果user1为u,则将user2和两者之间的pearson系数存入数组susers
            susers.append((pearson[2], pearson[3], pearson[4]))
        elif int(pearson[2]) == int(u):   #如果user2为u,则将user1和两者之间的pearson系数存入数组susers
            susers.append((pearson[1], pearson[3], pearson[4]))
    for movie in movies:  #进入循环，每次提取测试集中用户u看过的电影集中的一部电影，预测u对其的打分
        sum1 = 0
        sum2 = 0
        avg1 = avg(u)
        # s[i][0] :userid s[i][1]: pearson
        count = 0
        #print(movie)
        for suser in susers:
            #print(suser)
            #suser[0]为和u看过10部以上电影且pearson>0的用户
            sql = "select rating from u_base where userId=%d and movieID=%d" % (suser[0], int(movie[0]))
            cursor.execute(sql)
            result = cursor.fetchone()
            #print(result)
            #print(result)
            if result is not None:   #排除不存在这样用户的情况
                avg2 = avg(int(suser[0]))
                sum1 += suser[1] * (result[0] - avg2)
                sum2 += suser[1]
                count += 1
                #print("sum1:" + str(sum1))
                #print("sum2:" + str(sum2))
            if count == 10:
                break
        if sum1==0:
            predict = avg1
        else:
            predict = avg1 + (sum1 / sum2)
        print("用户%d对电影%d的预测打分为：%f" % (u,int(movie[0]), predict))
        sql = "insert into u_pred2(userId ,movieID ,pred) values (%d,%d,%f)" % ( u, int(movie[0]),predict)
        cursor.execute(sql)
        conn.commit()

def run(m,n):
    conn = mysql.connector.connect(host="localhost",
                                   user="root", password="960516",
                                   db="movielens_100k", charset="utf8")  # conn为连接到的数据库
    cursor = conn.cursor()

    for i in range(m,n):
        sql = "select movieId from u_test where userId=%d" % i  #提取用户i看过的电影集ms
        cursor.execute(sql)
        ms = cursor.fetchall()
        pred(i, ms)   #调用预测函数

if __name__ == '__main__':
    t1 = threading.Thread(target=run, args=(1, 100))
    t2 = threading.Thread(target=run, args=(100, 170))
    t3 = threading.Thread(target=run, args=(170, 220))
    t4 = threading.Thread(target=run, args=(220, 280))
    t5 = threading.Thread(target=run, args=(280, 350))
    t6 = threading.Thread(target=run, args=(350, 450))
    t7 = threading.Thread(target=run, args=(450, 550))
    t8 = threading.Thread(target=run, args=(550, 620))
    t9 = threading.Thread(target=run, args=(620, 700))
    t10 = threading.Thread(target=run, args=(700, 800))
    t11 = threading.Thread(target=run, args=(800, 880))
    t12 = threading.Thread(target=run, args=(880, 944))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()


