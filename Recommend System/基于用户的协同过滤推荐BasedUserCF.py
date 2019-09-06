#-*-coding:utf-8-*-
'''
Created on 2017��5��2��

@author: Jimmy Zhao
'''
from math import sqrt

fp = open("uid_score_bid.dat","r")

users = {}

for line in open("uid_score_bid.dat"):
    lines = line.strip().split(",")
    if lines[0] not in users:
        users[lines[0]] = {}
    users[lines[0]][lines[2]]=float(lines[1])


#----------------���������END----------------------



class recommender:
    #data�����ݼ�������ָusers
    #k����ʾ�ó��������k�Ľ���
    #metric����ʾʹ�ü������ƶȵķ���
    #n����ʾ�Ƽ�book�ĸ���
    def __init__(self, data, k=3, metric='pearson', n=10):

        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}

        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        if type(data).__name__ == 'dict':
            self.data = data
      
    def convertProductID2name(self, id):

        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    #����ļ������ƶȵĹ�ʽ���õ���Ƥ��ѷ���ϵ�����㷽��
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        
        #Ƥ��ѷ���ϵ�����㹫ʽ 
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n)  * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator
    
    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],self.data[instance])
                distances.append((instance, distance))

        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        return distances
    
    #�Ƽ��㷨�����庯��
    def recommend(self, user):
        #����һ���ֵ䣬�����洢�Ƽ����鵥�ͷ���
        recommendations = {}
        #�����user�����������û������ƶȣ�����һ��list
        nearest = self.computeNearestNeighbor(user)
#         print nearest
        
        userRatings = self.data[user]
#         print userRatings
        totalDistance = 0.0
        #��ס�����k�����ڵ��ܾ���
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance==0.0:
            totalDistance=1.0
            
        #����user�������k������userû�п��������Ƽ���user����������������һ�������ļ�������
        for i in range(self.k):
            
            #��i���˵���user�����ƶȣ�ת����[0,1]֮��
            weight = nearest[i][1] / totalDistance
            
            #��i���˵�name
            name = nearest[i][0]

            #��i���û������������Ӧ�Ĵ��
            neighborRatings = self.data[name]

            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = (recommendations[artist]+ neighborRatings[artist] * weight)

        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v)for (k, v) in recommendations]
        
        #����һ������
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

#         print recommendations[:self.n],"-------"
        return recommendations[:self.n]

def adjustrecommend(id):
    bookid_list = []
    r = recommender(users)
    print "�û�id:",id
    k = r.recommend("%s" % "changanamei")
    print "�Ƽ�book:",k
    for i in range(len(k)):
        bookid_list.append(k[i][0])
    print bookid_list
        
if __name__ == '__main__':
   adjustrecommend(2)