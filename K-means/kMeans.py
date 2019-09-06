#coding:utf-8
'''
Created on 2017��7��9��

@author: Jimmy Zhao
'''
import numpy as np

def kMeans(X, k, maxIt):
    #��������
    numPoints, numDim = X.shape
    dataSet = np.zeros((numPoints, numDim + 1))
    dataSet[: ,: -1 ] = X
    #��������µ����ĵ�
    centroids = dataSet[np.random.randint(numPoints, size = k), :]
    #centroids = dataSet[0:2,:]
    #��k�����ĵ��ǩ��ֵΪ[1��k+1]
    centroids[:, -1] = range(1, k+1)
    
    iterations = 0 #ѭ������
    oldCentroids = None  #��������ɵ����ĵ�
    
    while not shouldStop(oldCentroids, centroids, iterations, maxIt):
        print "iterations:\n ",iterations
        print "dataSet: \n",dataSet
        print "centroids:\n ",centroids
        
        #��copy��ԭ���ǽ��и��ƣ�����=����Ϊ=�൱��ͬʱָ��һ����ַ��һ���ı�����һ��Ҳ��ı�
        oldCentroids = np.copy(centroids)
        iterations += 1
        
        #�������ĵ�
        updataLabels(dataSet, centroids)
        
        #�õ��µ����ĵ�
        centroids = getCentroids(dataSet, k)
    
    return dataSet
    
def shouldStop(oldCentroids, centroids, iterations, maxIt):
    if iterations > maxIt:
        return True
    return np.array_equal(oldCentroids, centroids)


def updataLabels(dataSet, centroids):
    numPoints, numDim = dataSet.shape
    for i in range(0,numPoints):
        dataSet[i,-1] = getLabelFromCloseestCentroid(dataSet[i, :-1],centroids)
        

def getLabelFromCloseestCentroid(dataSetRow, centroids):
    label = centroids[0, -1]
    #np.linalg.norm() ������������֮��ľ���
    minDist = np.linalg.norm(dataSetRow - centroids[0, :-1])
    for i in range(1,centroids.shape[0]):
        dist = np.linalg.norm(dataSetRow - centroids[i,:-1])
        if dist < minDist:
            minDist = dist
            label = centroids[i,-1]
            
        print "minDist :\n" ,minDist
        return label
    
    
def getCentroids(dataSet, k):
    result = np.zeros((k, dataSet.shape[1]))
    for i in range(1, k+1):
        oneCluster = dataSet[dataSet[:,-1] == i,:-1]
        result[i - 1, :-1] = np.mean(oneCluster, axis=0)
        result[i - 1, -1] = i
        
    return result


x1 = np.array([1, 1])
x2 = np.array([2, 1])
x3 = np.array([4, 3])
x4 = np.array([5, 4])
testX = np.vstack((x1, x2, x3, x4))

result = kMeans(testX, 2, 10)
print "final result: \n",result