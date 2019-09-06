#-*-coding:utf-8-*-
'''
Created on 2017��5��9��

@author: Jimmy Zhao
'''

#����һ��������������ÿһ�����
class treeNode:
    def __init__(self,nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}   #���ڴ�Žڵ���ӽڵ�
        self.nodeLink = None #�����������Ƶ�Ԫ����
    
    #��count�������Ӹ���ֵ
    def inc(self, numOccur):
        self.count += numOccur
     
    #���ڽ������ı���ʽ��ʾ�����ڹ�������˵��������Ҫ��   
    def disp(self, ind = 1):
        print "  " * ind, self.name, "  ",self.count
        for child in self.children.values():
            child.disp(ind + 1)

#FP���Ĺ�������
def createTree(dataSet, minSup=1):
    ''' ����FP�� '''
    # ��һ�α������ݼ�������ͷָ���
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # �Ƴ���������С֧�ֶȵ�Ԫ����
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    # ��Ԫ�ؼ������ؿ�
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # ����һ����������ڴ��ָ������Ԫ����ָ��
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None) # ���ڵ�
    # �ڶ��α������ݼ�������FP��
    for tranSet, count in dataSet.items():
        localD = {} # ��һ���tranSet����¼����ÿ��Ԫ�����ȫ��Ƶ�ʣ���������
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # ע�����[0]����Ϊ֮ǰ�ӹ�һ��������
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)] # ����
            updateTree(orderedItems, retTree, headerTable, count) # ����FP��
    return retTree, headerTable

def updateTree(items, inTree, headerTable,count):
    #�ж������еĵ�һ��Ԫ�����Ƿ���Ϊ�ӽڵ���ڣ������������¸�Ԫ����ļ���
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    #��������ڣ��򴴽�һ���µ�treeeNode��������Ϊ�ӽڵ���ӵ�����    
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        # ����ͷָ����ǰһ������Ԫ����ڵ��ָ��ָ���½ڵ�
        if headerTable[items[0]][1]==None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
     # ��ʣ�µ�Ԫ�����������updateTree����            
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)    

#��ȡͷָ����и�Ԫ�����Ӧ�ĵ������β�ڵ㣬Ȼ����ָ���½ڵ�targetNode            
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode   

#�������ݼ�
def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict
#=========================================================

#����Ԫ��������һ������ģʽ����ǰ׺·����
#basePat��ʾ�����Ƶ���treeNodeΪ��ǰFP���ж�Ӧ�ĵ�һ���ڵ㣨���ں����ⲿͨ��headerTable[basePat][1]��ȡ��
def findPrefixPath(basePat,treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []     
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    #���غ���������ģʽ��
    return condPats

#����������ֱ���޸�prefixPath��ֵ������ǰ�ڵ�leafNode��ӵ�prefixPath��ĩβ��Ȼ��ݹ�����丸�ڵ�
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)    
        
#�ݹ����Ƶ���
#������inTree��headerTable����createTree()�������ɵ����ݼ���FP��
#    : minSup��ʾ��С֧�ֶ�
#    ��preFix�봫��һ���ռ��ϣ�set([])�������ں��������ڱ��浱ǰǰ׺
#    ��freqItemList�봫��һ�����б�[]�����������������ɵ�Ƶ���
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p:p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myConTree,myHead = createTree(condPattBases, minSup)
        
        if myHead != None:
            #���ڲ���
            print 'conditional tree for :', newFreqSet
            myConTree.disp()
            
            mineTree(myConTree, myHead, minSup, newFreqSet, freqItemList)

#��װ�㷨
def fpGrowth(dataSet, minSup=3):
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems

if __name__=="__main__":
    
    #���Լ������ݼ�������������
    '''
    simpDat = loadSimpDat()
    initSet = createInitSet(simpDat)
    myFPtree, myHeaderTab = createTree(initSet, 3)
    print myFPtree.disp()
    '''
    #����findPrefixPath����
    '''
    print "x",findPrefixPath('x', myHeaderTab['x'][1])
    print "z",findPrefixPath('z', myHeaderTab['z'][1])
    print "r",findPrefixPath('r', myHeaderTab['r'][1])
    '''
    #����mineTree�Ĵ���
    '''
    freqItems = []
    mineTree(myFPtree,  myHeaderTab, 3, set([]), freqItems)
    print freqItems
    '''
    #��װ�㷨��������
    dataSet = loadSimpDat()
    freqItems = fpGrowth(dataSet)
    print freqItems
    