import numpy as np
import pandas as pd
import math

u_test=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/test.csv",sep=';')
u_train=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/train.csv",sep=';')
test=pd.DataFrame(u_test)
train=pd.DataFrame(u_train)
test.columns = ["userId", "movieId", "rating", "timestamp"]
train.columns = ["userId", "movieId", "rating", "timestamp"]
pred=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/pred.csv")


def mae(test,pred):
    sum=0
    for i in range(0,10439):
        sum = sum + abs(test.iloc[i]['rating']-pred.iloc[i]['pred'])
        #print("test:" + str(test.iloc[i]['rating']))
        #print("pred:"+str(pred.iloc[i]['pred']))
    mae = sum / 10439  # 计算mae
    print("预测结果集与测试结果集的平均绝对误差为：%f" % mae)
    return mae

if __name__ == '__main__':
    mae(test,pred)