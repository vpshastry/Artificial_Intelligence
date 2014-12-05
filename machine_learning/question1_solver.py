from pprint import pprint
import math
import operator


class Question1_Solver:
    def __init__(self):
        self.data = []
        self.tree = None
        self.learn('train.data')
        print(self.labels)
        pprint(self.tree)
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
            nfeature=len(self.data[0])
            self.labels=["att"+str(i) for i in range(nfeature-1)]
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

    def chooseBestFeatureToSplit(self, dataset):
        numberFeature=len(dataset[0])-1
        baseEntropy=self.entropy(dataset)
        bestInfoGain=0.0
        bestFeature=-1
        for i in range(numberFeature):
            featureList=[x[i] for x in dataset]
            uniqueValues=set(featureList)
            newEntropy=0.0
            for value in uniqueValues:
                subDataset=self.splitDataset(dataset, i, value)
                prob=len(subDataset)/float(len(dataset))
                newEntropy += prob*self.entropy(subDataset)
            infoGain=baseEntropy-newEntropy
            if infoGain > bestInfoGain:
                bestInfoGain=infoGain
                bestFeature=i
        return bestFeature

    def buildTree(self, dataset,labels):
        classlist=[ x[-1] for x in dataset]
        if classlist.count(classlist[0]) == len(classlist):
            return classlist[0]
        if len(classlist)==1:
            return self.majority_count(classlist)
        bestFeature=self.chooseBestFeatureToSplit(dataset)
        bestFeatureLabel=labels[bestFeature]
        tree={bestFeatureLabel:{}}
        del(labels[bestFeature])
        featValues = [x[bestFeature] for x in dataset]
        uniqueVals = set(featValues)
        for value in uniqueVals:
            subLabels = labels[:]
            tree[bestFeatureLabel][value] = self.buildTree(self.splitDataset(dataset, bestFeature, value),subLabels)
        return tree

    def classify(self, tree,labels,testvec):
        #print('testvec-', testvec)
        firstStr = tree.keys()[0]
        #print(firstStr)
        #print(labels)
        secondDict = tree[firstStr]
        featIndex = labels.index(firstStr)
        #print(featIndex)
        for key in secondDict.keys():
            #print(featIndex)
            if testvec[featIndex] == key:
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = self.classify(secondDict[key],labels,testvec)
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
            nfeature=len(self.data[0])
            labels2=["att"+str(i) for i in range(nfeature-1)]
            predicted_label = self.classify(self.tree, labels2, final_instances)
            #print(predicted_label)
            return predicted_label