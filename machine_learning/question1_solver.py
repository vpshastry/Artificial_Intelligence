from pprint import pprint
import math
import operator


class Question1_Solver:
    def __init__(self):
        self.data = []
        self.tree = None
        self.learn('train.data')
        #print(self.labels)
        #pprint(self.tree)
        self.count = 0
        self.attributes = ['handicapped-infants', 'water-project-cost-sharing', 'adoption-of-the-budget-resolution', 'physician-fee-freeze', 'el-salvador-aid', 'religious-groups-in-schools', 'anti-satellite-test-ban', 'aid-to-nicaraguan-contras', 'mx-missile', 'immigration', 'synfuels-corporation-cutback', 'education-spending', 'superfund-right-to-sue', 'crime', 'duty-free-exports', 'export-administration-act-south-africa', 'class']
        return

    # Add your code here.
    # Read training data and build your decision tree
    # Store the decision tree in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'

    #find most common value for an attribute
    def learn(self, train_data):
        with open(train_data, "r") as f:
            data = f.read().splitlines()
        target_class = "class"
        for row in data:
            instance = row.split()
            target =  instance[0]
            dataList = instance[1].split(',')
            dataList.append(target)
            self.data.append(dataList)
            colnums=len(self.data[0])
            self.labels=["att"+str(i) for i in range(colnums-1)]
        self.tree = self.buildTree(self.data,self.labels)
        return
    #find most common value for an attribute
    def majority_count(self, classlist):
        classcount={}
        for value in classlist:
            if value not in classcount.keys():
                classcount[value]=0
            classcount[value] += 1
        sortedClassCount=sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
        return sortedClassCount[0][0]
    #Calculates the entropy of the given data set for the target attr(last)
    def entropy(self, dataset):
        n=len(dataset)
        labels={}
        for record in dataset:
            label=record[-1]
            if label not in labels.keys():
                labels[label]=0
            labels[label]+=1
        entropy=0.0
        for key in labels.keys():
            prob=float(labels[key])/n
            entropy= -prob*math.log(prob,2)
        return entropy
    #splitting a list of instances according to their values of a specified attribute
    def splitDataset(self, dataset,col,value):
        retDataSet=[]
        for record in dataset:
            if record[col] == value:
                reducedRecord=record[:col]
                reducedRecord.extend(record[col+1:])
                retDataSet.append(reducedRecord)
        return retDataSet
    #choose best attribute to split on...
    def chooseBestAttr(self, dataset):
        num_attrs=len(dataset[0])-1
        baseEntropy=self.entropy(dataset)
        bestInfoGain=0.0
        bestAttr=-1
        for i in range(num_attrs):
            attrList=[x[i] for x in dataset]
            uniqueValues=set(attrList)
            newEntropy=0.0
            for value in uniqueValues:
                subset=self.splitDataset(dataset, i, value)
                prob=len(subset)/float(len(dataset))
                newEntropy += prob*self.entropy(subset)
            infoGain=baseEntropy-newEntropy
            if infoGain > bestInfoGain:
                bestInfoGain=infoGain
                bestAttr=i
        return bestAttr
    #Create the DTree
    def buildTree(self, dataset,labels):
        classlist=[ x[-1] for x in dataset]
        if classlist.count(classlist[0]) == len(classlist):
            return classlist[0]
        if len(classlist)==1:
            return self.majority_count(classlist)
        bestAttr=self.chooseBestAttr(dataset)
        bestFeatureLabel=labels[bestAttr]
        tree={bestFeatureLabel:{}}
        del(labels[bestAttr])
        AttrValues = [x[bestAttr] for x in dataset]
        uniqueVals = set(AttrValues)
        for value in uniqueVals:
            subLabels = labels[:]
            tree[bestFeatureLabel][value] = self.buildTree(self.splitDataset(dataset, bestAttr, value),subLabels)
        return tree
    # test, using built tree to classify test queries
    def classify(self, tree,labels,test_query):
        firstStr = tree.keys()[0]
        secondDict = tree[firstStr]
        AttrIndex = labels.index(firstStr)
        #print(featIndex)
        for key in secondDict.keys():
            #print(featIndex)
            if test_query[AttrIndex] == key:
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = self.classify(secondDict[key],labels,test_query)
                else: classLabel = secondDict[key]
        try:
            return classLabel
        except:
            return "republican"

    def solve(self, query):
            #pprint(self.tree)
            instances = query.split()
            #instances
            #print(instances[0])
            final_instances = instances[0].split(',')
            #print('final_inst-', final_instances)
            colnums=len(self.data[0])
            cols2=["att"+str(i) for i in range(colnums-1)]
            predicted_label = self.classify(self.tree, cols2, final_instances)
            #print(predicted_label)
            return predicted_label
