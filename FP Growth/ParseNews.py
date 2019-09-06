#-*-coding:utf-8-*-
'''
Created on 2017��5��9��

@author: Jimmy Zhao
'''
import FP_Tree

#�����ݼ����ص��б�
parsedDat = [line.split() for line in open('kosarak.dat').readlines()]
print parsedDat

#��ʼ���ϸ�ʽ��
initSet = FP_Tree.createInitSet(parsedDat)

#����FP��
myFPtree, myHeaderTab = FP_Tree.createTree(initSet, 100000)

#�������б�����Ƶ���
myFreqList = []
FP_Tree.mineTree(myFPtree, myHeaderTab, 100000, set([]), myFreqList)
print len(myFreqList)
print myFreqList