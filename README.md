1.基础算法
数据集：按照用户评分时间1:9划分数据集，训练集89561，测试集10439
相似度算法：pearson系数，通过两个用户共同看过的电影计算相似度，若两用户没有共同看过电影，相似度设为0
预测值算法：选取相似度>0，且共同看过5部以上的电影的用户标记为相似用户。例如在预测user1对item2打分时，选取最多10个相似用户对item2的打分进行预测，若相似用户均未看过item2，则用user1的平均打分值取代对item2的打分。

2.相似度改进
（1）低分是否更有价值
（2）高分是否更有价值
（3）用户之间共同看过的电影数越多，是否就更相似
     公式：新的相似度=皮尔森系数 +  a * (共同看过电影数-16)
     其中16表示每两位用户之间平均共同看过电影16部
     a表示用户之间每多共同看过一部电影会增加的单位系数

3.结果
    
算法	Mae值	Mae变化
基础算法	0.790863	0
只考虑低分（低分低于3.58）	0.832089	+0.041226
只考虑高分（高分高于3.58）	0.912564	+0.121701
考虑共同看过的电影数的影响（a=0.005）	0.897767	+0.106904
考虑共同看过的电影数的影响（a=0.004）		

4.验证
   提取user1为u或者user2为u的用户与其他用户之间的相似度，其中要求两用户之间的相似度>0且共同看过5部以上电影
（1）Pandas实现
 simi = df[((df['user1'] == a) | (df['user2'] == a)) & (df['count'] >= 5) & (df['similarity'] > 0)].sort_values(
    by="similarity", axis=0, ascending=False)

（2）连接数据库实现
sql = "select * from pearson3 where (user1=%d or user2=%d) and count>=5 and pearson>0 order by pearson desc" % (u, u)
cursor.execute(sql)
pearsons = cursor.fetchall()

（3）多线程运行

5.Surprise库
   Surprise库自带了SVD推荐算法，SVD是一种基于隐语义的协同过滤算法。
（1）计算mae

#下载surprise自带数据集
data = Dataset.load_builtin('ml-100k')
#k折交叉验证，k取5
data.split(n_folds=5)
# SVD矩阵分解
algo = SVD()
mae = model_selection.cross_validate(algo, data, measures=['MAE'])
print(mae)



（2）计算预测值
#需要通过data.build_full_trainset()将Dataset结构转换为Trainset这样的数据结构
trainset = data.build_full_trainset()
algo.fit(trainset)
uid = str(1)
mid = str(168)
pred = algo.predict(uid, mid)
print('用户%s对电影%s的预测评分为：%f' %(pred[0],pred[1],pred[3]))
