import numpy as np
import pandas as pd
import math
import threading

#添加数据集
u_test=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/test.csv",sep=';')
u_train=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/train.csv",sep=';')
test=pd.DataFrame(u_test)
train=pd.DataFrame(u_train)
train.columns = ["userId", "movieId", "rating", "timestamp"]

#pearson系数计算
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

#计算用户之间的相似度
def similarity(a,b):
    user1 = train[train['userId'] == a][["movieId", "rating"]].sort_values(by="movieId", axis=0)
    user2 = train[train['userId'] == b][["movieId", "rating"]].sort_values(by="movieId", axis=0)
    m = 0
    n = 0
    rate1 = []  # 用户i的打分数组
    rate2 = []  # 用户j的打分数组
    while (m < len(user1)) and (n < len(user2)):
        #用户1和用户2均看过该电影且评分低于3.5
        if (user1.iloc[m]['movieId'] == user2.iloc[n]['movieId']): #and (user1.iloc[m]['rating']<=3.580595):
            rate1.append(user1.iloc[m]['rating'])
            rate2.append(user2.iloc[n]['rating'])
            m += 1
            n += 1
        elif user1.iloc[m]['movieId'] < user2.iloc[n]['movieId']:
            m += 1
        else:
            n += 1
    if len(rate1) != 0:
        simliarity = pearson(rate1, rate2)
        #if len(rate1) >= 16:
            #simliarity = simliarity + 0.048 * (len(rate1) - 16)
        #else:
            #simliarity = simliarity - 0.048 * (16 - len(rate1))
        print("用户%d与用户%d的pearson系数为：%f" % (a, b, simliarity))
        return simliarity,len(rate1)
    else:  # 若没有共同打分的电影
        simliarity = 0.000000  # 相似度为0，并存入数据库表格pearson1
        print("用户%d与用户%d的pearson系数为：%f" % (a, b, simliarity))
        return simliarity,0


def table_similarity(m,n):
    df = pd.DataFrame()

    for a in range(m,n):  # 获取用户i的打分情况
        for b in range(m+ 1,944):
            simi,count=similarity(a, b)
            df_insert = {
                'user1': pd.Series(a),
                'user2': pd.Series(b),
                'similarity': pd.Series(simi),
                'count':pd.Series(count)
            }
            df_insert = pd.DataFrame(df_insert)
            df = df.append(df_insert, ignore_index=True)

    print(df)
    return df


if __name__ == '__main__':
    table_similarity(1,944).to_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/similarity2.csv",index=False)





