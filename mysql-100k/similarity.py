import math
import mysql.connector
import threading


# 计算user1 和 user2的皮尔森系数

def pearson(vector1, vector2):
    n = len(vector1)
    #simple sums
    sum1 = sum(float(vector1[i]) for i in range(n))
    sum2 = sum(float(vector2[i]) for i in range(n))
    #sum up the squares
    sum1_pow = sum([pow(v, 2.0) for v in vector1])
    sum2_pow = sum([pow(v, 2.0) for v in vector2])
    #sum up the products
    p_sum = sum([vector1[i]*vector2[i] for i in range(n)])
    #分子num，分母den
    num = p_sum - (sum1*sum2/n)
    den = math.sqrt((sum1_pow-pow(sum1, 2)/n)*(sum2_pow-pow(sum2, 2)/n))
    if den == 0:
        return 0.0
    return num/den

def run(s,t):
    # 建立数据库连接获取数据
    conn = mysql.connector.connect(host="localhost",
                                   user="root", password="960516",
                                   db="movielens_100k", charset="utf8")  # conn为连接到的数据库
    cursor = conn.cursor()

    for a in range(s, t):  # 获取用户i的打分情况
        for b in range(a+1, 944):
            sql = 'select movieId,rating from u_base where userId=%d order by movieId asc' % a  # 按照userID升序提取出用户看过的电影movieId和评分rate
            cursor.execute(sql)  # 执行SQL并从数据库获取结果
            user1 = cursor.fetchall()  # 获取所有结果集，user1[][]是一组两列的数据集，第一列为电影序列，第二列为打分
            sql = 'select movieId,rating from u_base where userId=%d order by movieId asc' % b
            cursor.execute(sql)
            user2 = cursor.fetchall()
            n = 0  # n记录用户j打分记录数
            m = 0  # m记录用户i打分记录数
            rate1 = []  # 用户i的打分数组
            rate2 = []  # 用户j的打分数组
            while (m <= len(user1) - 1) and (n <= len(user2) - 1):  # 读取用户i和j的打分记录
                if (user1[m][0] == user2[n][0]): #and (user1[m][1] >= 3.580595):   #低分设置条件
                    rate1.append(user1[m])
                    rate2.append(user2[n])
                    m += 1
                    n += 1
                elif user1[m][0] < user2[n][0]:
                    m += 1
                else:
                    n += 1
            if len(rate1) != 0:    #如果共同打分的电影，len(rate1)为共同打分的电影数
                p1 = []
                p2 = []
                for i in rate1:
                    p1.append(i[1])
                for i in rate2:
                    p2.append(i[1])
                simliarity = pearson(p1, p2)   #用共同打分的电影计算两个用户之间的相似度，并存入数据库表格pearson；
                if len(rate1) >= 16:
                    simliarity = simliarity + 0.004 * (len(rate1) - 16)
                else:
                    simliarity = simliarity - 0.004 * (16 - len(rate1))
                print("用户%d与用户%d的pearson系数为：%f" % (a, b, simliarity))
                sql = "insert into pearson3 (user1, user2, pearson, count) values (%d, %d, %f, %d)" % (a, b, float(simliarity), len(rate1))
                cursor.execute(sql)
                conn.commit()
            else:   #若没有共同打分的电影
                simliarity=0.000000    #相似度为0，并存入数据库表格pearson1
                print("用户%d与用户%d的pearson系数为：%f" % (a, b, simliarity))
                sql = "insert into pearson3(user1, user2, pearson, count) values (%d, %d, %f, %d)" % (a, b, float(simliarity), 0)
                cursor.execute(sql)
                conn.commit()

if __name__=='__main__':

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

