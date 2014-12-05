from pprint import pprint
import math
import operator


class Question1_Solver:
    def __init__(self):
        self.attributes = ['handicapped-infants', 'water-project-cost-sharing', 'adoption-of-the-budget-resolution', 'physician-fee-freeze', 'el-salvador-aid', 'religious-groups-in-schools', 'anti-satellite-test-ban', 'aid-to-nicaraguan-contras', 'mx-missile', 'immigration', 'synfuels-corporation-cutback', 'education-spending', 'superfund-right-to-sue', 'crime', 'duty-free-exports', 'export-administration-act-south-africa', 'class']
        self.data = []
        self.tree = None
        self.learn('train.data')
        #print(self.labels)
        #pprint(self.tree)
        self.count = 0

        return

    # Add your code here.
    # Read training data and build your decision tree
    # Store the decision tree in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'

    #find most common value for an attribute
    def learn(self, train_data):
        data = []
        with open(train_data, "r") as f:
            data = f.read().splitlines()
        target_class = "class"
        for row in data:
            instance = row.split()
            target =  instance[0]
            dataList = instance[1].split(',')
            dataList.append(target)
            self.data.append(dataList)
            col_nums=len(self.data[0])
            self.labels=[self.attributes[i] for i in range(col_nums-1)]
        self.tree = self.buildTree(self.data,self.labels)
        return

    #find most common value for an attribute
    def majority_count(self, classlist):
        #print classlist
        classcount={}
        for value in classlist:
            if value not in classcount.keys():
                classcount[value]=0
            classcount[value] += 1
        freq_max = -99999999
        res = None
        for i in classcount:
           if classcount[i] > freq_max:
               freq_max = classcount[i]
               res = i
        return res

    #Calculates the entropy of the given data set for the target attr(last)
    def entropy(self, dataset):
        labels={}
        entropy=0.0

        for record in dataset:
            label=record[-1]
            if label not in labels.keys():
                labels[label]=0
            labels[label]+=1

        for key in labels.keys():
            prob = float(labels[key]) /len(dataset)
            entropy += - prob *math.log (prob, 2)
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
        num_attrs = len(dataset[0])-1
        baseEntropy =self.entropy(dataset)
        maxInfoGain=0.0
        bestAttr=-1

        for i in range(num_attrs):
            attrList=[x[i] for x in dataset]
            uniqueValues=set(attrList)
            newEntropy=0.0

            for value in uniqueValues:
                prob=len(self.splitDataset(dataset, i, value))/float(len(dataset))
                newEntropy += prob*self.entropy(self.splitDataset(dataset, i, value))

            infoGain=baseEntropy-newEntropy

            if infoGain > maxInfoGain:
                maxInfoGain=infoGain
                bestAttr=i

        return bestAttr

    #Create the DTree
    def buildTree(self, dataset,labels):
        classlist = []
        for i in dataset:
            classlist.append(i[-1])

        if classlist.count(classlist[0]) == len(classlist):
            return classlist[0]

        if len(classlist) is 1:
            return self.majority_count(classlist)

        bestAttr=self.chooseBestAttr(dataset)
        bestFeatureLabel=labels[bestAttr]
        tree={bestFeatureLabel:{}}

        labels.pop (bestAttr)

        AttrValues = []
        for i in dataset:
            AttrValues.append(i[bestAttr])

        uniqueVals = set(AttrValues)

        for value in uniqueVals:
            subLabels = list(labels)
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
                if isinstance(secondDict[key], dict):
                    classification = self.classify(secondDict[key], labels, test_query)
                else:
                    classification = secondDict[key]
        try:
            return classification
        except:
            return "republican" #default

    def solve(self, query):
            #pprint(self.tree)
            instances = query.split()
            #instances
            #print(instances[0])
            final_instances = instances[0].split(',')
            #print('final_inst-', final_instances)
            col_nums=len(self.data[0])
            cols2 = [self.attributes[i] for i in range(col_nums-1)]
            predicted_label = self.classify(self.tree, cols2, final_instances)
            #print(predicted_label)
            return predicted_label
