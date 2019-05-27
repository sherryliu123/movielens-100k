import numpy as np
import pandas as pd
import math


u_test=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/test.csv",sep=';')
u_train=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/train.csv",sep=';')
test=pd.DataFrame(u_test)
train=pd.DataFrame(u_train)
test.columns = ["userId", "movieId", "rating", "timestamp"]
train.columns = ["userId", "movieId", "rating", "timestamp"]
df=pd.read_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/similarity1.csv")

def avg(a):
    ratings=pd.DataFrame()
    rating=[]
    n=len(train[train['userId']==a]['rating'])
    for i in range(0,n):
        rating.append(train[train['userId']==a]['rating'].iloc[i])
    return np.mean(rating)

#print([((df['user1']==1)|(df['user2']==1))&(df['count']>=5)]['similarity'].sort_values(by="similarity", axis=1))

def pred(a,p):
    simi = df[((df['user1'] == a) | (df['user2'] == a)) & (df['count'] >= 5) & (df['similarity'] > 0)].sort_values(
        by="similarity", axis=0, ascending=False)
    #print(simi)
    sim1=0
    sim2=0
    cout=0
    for j in range(0, len(simi)):
        if a == simi.iloc[j]['user1']:
            b= simi.iloc[j]['user2']
            sim_ab = simi.iloc[j]['similarity']
        elif a == simi.iloc[j]['user2']:
            b= simi.iloc[j]['user1']
            sim_ab = simi.iloc[j]['similarity']
        r_bp=train[(train['userId']==b)&(train['movieId']==p)]['rating']
        #print(r_bp)
        if any(r_bp) == True:
            sim1 += float(sim_ab) * (float(r_bp) - float(avg(b)))
            sim2 += sim_ab
            cout +=1
            #print("sim1:"+ str(sim1))
            #print("sim2:" + str(sim2))
        if cout==10:
            break
    if sim1==0 :
        pred=avg(a)
    else:
        pred = avg(a) + sim1/sim2
    print("user%d对movie%d的预测打分为%f" %(a,p,pred))
    return pred

def extract():
    predict=pd.DataFrame()
    ms=[]
    for  u in range(1,944):
        ms=test[test['userId']==u]['movieId']
        for m in ms:
            pred_insert={
                'userId':pd.Series(u),
                'movieId':pd.Series(m),
                'pred':pd.Series(pred(u,m))
            }
            pred_insert=pd.DataFrame(pred_insert)
            predict=predict.append(pred_insert, ignore_index=True)
    #print(predict)
    return predict

if __name__ == '__main__':
    extract().to_csv("C:/Users/Administrator/Desktop/recommender-sys/movielens-100k/pred1.csv",index=False)