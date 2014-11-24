from collections import Counter
from pprint import pprint
import math
import node

class Question1_Solver:
    def __init__(self):
        self.data = []
        self.tree = None
        self.learn('train.data')
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
        # # remove trace=1 to turn off tracing
        #print tree
        with open(train_data, "r") as f:
            data = f.read().splitlines()
        target_class = "class"
        for row in data:
            instance = row.split()
            target =  instance[0]
            dataList = instance[1].split(',')
            dataList.append(target)
            self.data.append(dataList)
        attributes =['handicapped-infants', 'water-project-cost-sharing', 'adoption-of-the-budget-resolution', 'physician-fee-freeze', 'el-salvador-aid', 'religious-groups-in-schools', 'anti-satellite-test-ban', 'aid-to-nicaraguan-contras', 'mx-missile', 'immigration', 'synfuels-corporation-cutback', 'education-spending', 'superfund-right-to-sue', 'crime', 'duty-free-exports', 'export-administration-act-south-africa', 'class']
        #print self.data
        #print target
        self.tree = self.makeTree(self.data, attributes, target_class, 0)
        #pprint(self.tree)
        #data[x][0] - target
        #print(self.data[0][0])
        return

    #find item in a list
    def find(self, item, list):
        for i in list:
            if item(i):
                return True
            else:
                return False

    #find most common value for an attribute
    def majority(self, attributes, data, target):
        #find target attribute
        valFreq = {}
        #find target in data
        index = attributes.index(target)
        #calculate frequency of values in target attr
        for tuple in data:
            if (valFreq.has_key(tuple[index])):
                valFreq[tuple[index]] += 1
            else:
                valFreq[tuple[index]] = 1
        max = 0
        major = ""
        for key in valFreq.keys():
            if valFreq[key]>max:
                max = valFreq[key]
                major = key
        return major

    #Calculates the entropy of the given data set for the target attr
    def entropy(self, attributes, data, targetAttr):

        valFreq = {}
        dataEntropy = 0.0

        #find index of the target attribute
        i = 0
        for entry in attributes:
            if (targetAttr == entry):
                break
            ++i

        # Calculate the frequency of each of the values in the target attr
        for entry in data:
            if (valFreq.has_key(entry[i])):
                valFreq[entry[i]] += 1.0
            else:
                valFreq[entry[i]]  = 1.0

        # Calculate the entropy of the data for the target attr
        for freq in valFreq.values():
            dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2)

        return dataEntropy

    def gain(self, attributes, data, attr, targetAttr):
        """
        Calculates the information gain (reduction in entropy) that would
        result by splitting the data on the chosen attribute (attr).
        """
        valFreq = {}
        subsetEntropy = 0.0

        #find index of the attribute
        i = attributes.index(attr)

        # Calculate the frequency of each of the values in the target attribute
        for entry in data:
            if (valFreq.has_key(entry[i])):
                valFreq[entry[i]] += 1.0
            else:
                valFreq[entry[i]]  = 1.0
        # Calculate the sum of the entropy for each subset of records weighted
        # by their probability of occuring in the training set.
        for val in valFreq.keys():
            valProb        = valFreq[val] / sum(valFreq.values())
            dataSubset     = [entry for entry in data if entry[i] == val]
            subsetEntropy += valProb * self.entropy(attributes, dataSubset, targetAttr)

        # Subtract the entropy of the chosen attribute from the entropy of the
        # whole data set with respect to the target attribute (and return it)
        return (self.entropy(attributes, data, targetAttr) - subsetEntropy)

    #choose best attibute
    def chooseAttr(self, data, attributes, target):
        best = attributes[0]
        maxGain = 0;
        for attr in attributes:
            newGain = self.gain(attributes, data, attr, target)
            if newGain>maxGain:
                maxGain = newGain
                best = attr
        return best

    #get values in the column of the given attribute
    def getValues(self, data, attributes, attr):
        index = attributes.index(attr)
        values = []
        for entry in data:
            if entry[index] not in values:
                values.append(entry[index])
        return values

    def getExamples(self, data, attributes, best, val):
        examples = [[]]
        index = attributes.index(best)
        for entry in data:
            #find entries with the give value
            if (entry[index] == val):
                newEntry = []
                #add value if it is not in best column
                for i in range(0,len(entry)):
                    if(i != index):
                        newEntry.append(entry[i])
                examples.append(newEntry)
        examples.remove([])
        return examples

    def makeTree(self, data, attributes, target, recursion):
        recursion += 1
        #Returns a new decision tree based on the examples given.
        data = data[:]
        #print target
        #print(attributes.index(target))
        vals = [record[attributes.index(target)] for record in data]
        default = self.majority(attributes, data, target)

        # If the dataset is empty or the attributes list is empty, return the
        # default value. When checking the attributes list for emptiness, we
        # need to subtract 1 to account for the target attribute.
        if not data or (len(attributes) - 1) <= 0:
            return default
        # If all the records in the dataset have the same classification,
        # return that classification.
        elif vals.count(vals[0]) == len(vals):
            return vals[0]
        else:
            # Choose the next best attribute to best classify our data
            best = self.chooseAttr(data, attributes, target)
            # Create a new decision tree/node with the best attribute and an empty
            # dictionary object--we'll fill that up next.
            tree = {best:{}}

            # Create a new decision tree/sub-node for each of the values in the
            # best attribute field
            for val in self.getValues(data, attributes, best):
                # Create a subtree for the current value under the "best" field
                examples = self.getExamples(data, attributes, best, val)
                newAttr = attributes[:]
                newAttr.remove(best)
                subtree = self.makeTree(examples, newAttr, target, recursion)

                # Add the new subtree to the empty dictionary object in our new
                # tree/node we just created.
                tree[best][val] = subtree

        return tree


    # Add your code here.
    # Use the learned decision tree to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'democrat'

    def solve(self, query):
        self.count+=1
        #pprint(self.tree)
        tempDict = self.tree
        result = "*"
        while(isinstance(tempDict, dict)):
            root = node.Node(tempDict.keys()[0], tempDict[tempDict.keys()[0]])
            tempDict = tempDict[tempDict.keys()[0]]
            index = self.attributes.index(root.value)
            value = query[index]
            if(value in tempDict.keys()):
                child = node.Node(value, tempDict[value])
                result = tempDict[value]
                tempDict = tempDict[value]
            else:
                print("can't process input %s" % query)
                result = "?"
                break
        print ("entry%s = %s" % (self.count, result))
        return result
