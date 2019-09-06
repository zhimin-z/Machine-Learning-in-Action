#-*-coding:utf-8-*-
'''
Created on 2017��5��8��

@author: Jimmy Zhao
'''
from pydoc import apropos

#=========================     ׼������ ���£�      ==========================================
#�������ݼ�
def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def createC1(dataSet):
    C1 = []   #C1Ϊ��СΪ1����ļ���
    for transaction in dataSet:  #�������ݼ��е�ÿһ������
        for item in transaction: #����ÿһ�������е�ÿ����Ʒ
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    #map������ʾ����C1�е�ÿһ��Ԫ��ִ��forzenset��frozenset��ʾ���������ļ��ϣ������ɸı�
    return map(frozenset,C1)

#Ck��ʾ���ݼ���D��ʾ��ѡ���ϵ��б�minSupport��ʾ��С֧�ֶ�
#�ú������ڴ�C1����L1��L1��ʾ�������֧�ֶȵ�Ԫ�ؼ���
def scanD(D,Ck,minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            #issubset����ʾ�������can�е�ÿһԪ�ض���tid���򷵻�true  
            if can.issubset(tid):
                #ͳ�Ƹ�������scan���ֵĴ���������ssCnt�ֵ��У��ֵ��key�Ǽ��ϣ�value��ͳ�Ƴ��ֵĴ���
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        #����ÿ�����֧�ֶȣ��������������Ѹ�����뵽retList�б���
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        #����֧�ֵ�����ֵ�
        supportData[key] = support
    return retList,supportData
#====================                ׼���������ϣ�              =============================

#======================          Apriori�㷨���£�               =================================
#Create Ck,CaprioriGen ()�����˲���ΪƵ����б�Lk���Ԫ�ظ���k�����ΪCk
def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            #ǰk-2����ͬʱ�ϲ���������
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
            
    return retList

def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)  #����C1
    #D: [set([1, 3, 4]), set([2, 3, 5]), set([1, 2, 3, 5]), set([2, 5])]
    D = map(set,dataSet)
    L1,supportData = scanD(D, C1, minSupport)
    L = [L1]
    #��������ĳ���Ϊk - 1,�����ǰk-2����ͬ�ſ����ӣ����󲢼�������[:k-2]��ʵ������Ϊȡ�б��ǰk-1��Ԫ��
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk,supK = scanD(D,Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k +=1
    return L,supportData
#======================          Apriori�㷨(��)               =================================


#========================            �����������ɺ���                     ========================
#�����±���������
#L����ʾƵ����б�supportData��������ЩƵ���֧�����ݵ��ֵ䣬minConf����ʾ��С���Ŷȷ�ֵ
def generateRules(L, supportData,minConf = 0.7):
    bigRuleList = [] #��ſ��Ŷȣ�������Ը��ݿ��Ŷ�����
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i>1):
                #������Ԫ����Ŀ����2����ʹ������ĺ�������������һ���ĺϲ����ϲ���������
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                #������ֻ������Ԫ�أ���ʹ������ĺ���������Ŷ�
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)    
            
    return bigRuleList

#��һ���޸ģ����ֶ�ʧ���Ǽ�����������
def generateRules2(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                # ����������Ԫ�صļ���
                H1 = calcConf(freqSet, H1, supportData, bigRuleList, minConf)
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                # ����Ԫ�صļ���
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

#�ڶ����޸ģ��򻯺������͵�һ���޸Ľ����ͬ
def generateRules3(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            rulesFromConseq2(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList
 
def rulesFromConseq2(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > m): # �жϳ��ȸ�Ϊ > m����ʱ��������H�Ŀ��Ŷ�
        Hmpl = calcConf(freqSet, H, supportData, brl, minConf)
        if (len(Hmpl) > 1): # �ж�������ŶȺ��Ƿ��п��Ŷȴ�����ֵ��������������һ��H
            Hmpl = aprioriGen(Hmpl, m + 1)
            rulesFromConseq2(freqSet, Hmpl, supportData, brl, minConf) # �ݹ���㣬����

#�������޸�       ����rulesFromConseq2()�����еĵݹ��ȥ���˶����Hmpl���������н����������ͬ
def rulesFromConseq3(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    while (len(freqSet) > m): # �жϳ��� > m����ʱ������H�Ŀ��Ŷ�
        H = calcConf(freqSet, H, supportData, brl, minConf)
        if (len(H) > 1): # �ж�������ŶȺ��Ƿ��п��Ŷȴ�����ֵ��������������һ��H
            H = aprioriGen(H, m + 1)
            m += 1
        else: # ���ܼ���������һ���ѡ����������ǰ�˳�ѭ��
            break

#�������Ŀ��Ŷȣ����ҵ�������С���ŶȵĹ�������prunedH�У���Ϊ����ֵ����
def calcConf(freqSet,H,supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet - conseq]
      
        if conf>= minConf:
            print freqSet-conseq,"-->",conseq ,"conf:",conf
            br1.append((freqSet-conseq,conseq,conf))  #�����Ŷ��б�
            prunedH.append(conseq)    #����������С���ŶȵĹ���
    return prunedH

#���������в�������Ĺ�������HΪ��ǰ�ĺ�ѡ���򼯣�������һ��ĺ�ѡ����
#freqSet��Ƶ��� H�����Գ����ڹ����Ҳ���Ԫ���б�  supportData���������֧�ֶȣ�brl�������ɵĹ�������minConf����С���Ŷȷ�ֵ
def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) >(m +1)):
        Hmp1 = aprioriGen( H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)          
        if (len(Hmp1) >1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)
        
        
if __name__=="__main__":
    dataSet = loadDataSet()
    L,suppData = apriori(dataSet)
    i = 0
    for one in L:
        print "����Ϊ %s ��Ƶ�����" % (i + 1), one,"\n"
        i +=1
        
    print "generateRules3��\nminConf=0.7ʱ��"
    rules = generateRules(L,suppData, minConf=0.7)
    print "\nminConf=0.5ʱ��"
    rules = generateRules(L,suppData, minConf=0.5)
    
    print "generateRules2��\nminConf=0.7ʱ��"
    rules = generateRules2(L,suppData, minConf=0.7)
    print "minConf=0.5ʱ��"
    rules = generateRules2(L,suppData, minConf=0.5)
    
    
    print "generateRules3��\nminConf=0.7ʱ��"
    rules = generateRules3(L,suppData, minConf=0.7)
    print "minConf=0.5ʱ��"
    rules = generateRules3(L,suppData, minConf=0.5)