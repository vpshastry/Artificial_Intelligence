from pprint import pprint
class Question2_Solver:
    def __init__(self):
        self.demrepubHash = dict()
        self.smoothValue = 0.25
        self.values = ['y', 'n', '?']
        self.targets = ['democrat', 'republican']
        self.data = []
        self.attributes =['handicapped-infants', 'water-project-cost-sharing', 'adoption-of-the-budget-resolution',
                          'physician-fee-freeze', 'el-salvador-aid', 'religious-groups-in-schools',
                          'anti-satellite-test-ban', 'aid-to-nicaraguan-contras', 'mx-missile', 'immigration',
                          'synfuels-corporation-cutback', 'education-spending', 'superfund-right-to-sue', 'crime',
                          'duty-free-exports', 'export-administration-act-south-africa', 'class']
        self.learn('train.data')
        return;

    def buildHashMap(self, data):
        for target in self.targets:
            for char in self.values:
                for curAttribute in self.attributes:
                    self.demrepubHash[(target, curAttribute, char)] = 0

        i = 0

        for column in zip(*data):
            print "Working on attribute: ", self.attributes[i]
            j = 0
            noOfdemQ = noOfdemN = noOfdemY = 0
            noOfrepQ = noOfrepN = noOfrepY = 0
            for char in column:
                if data[j][-1] == self.targets[0]:
                    if char is 'y':
                        noOfdemY = noOfdemY +1
                    elif char is 'n':
                        noOfdemN = noOfdemN +1
                    elif char is '?':
                        noOfdemQ = noOfdemQ +1

                elif data[j][-1] == self.targets[1]:
                    if char is 'y':
                        noOfrepY = noOfrepY +1
                    elif char is 'n':
                        noOfrepN = noOfrepN +1
                    elif char is '?':
                        noOfrepQ = noOfrepQ +1

                j = j +1

            self.demrepubHash[(self.targets[0], self.attributes[i], 'y')] = noOfdemY
            self.demrepubHash[(self.targets[0], self.attributes[i], 'n')] = noOfdemN
            self.demrepubHash[(self.targets[0], self.attributes[i], '?')] = noOfdemQ

            self.demrepubHash[(self.targets[1], self.attributes[i], 'y')] = noOfrepY
            self.demrepubHash[(self.targets[1], self.attributes[i], 'n')] = noOfrepN
            self.demrepubHash[(self.targets[1], self.attributes[i], '?')] = noOfrepQ
            i = i +1

        return

        '''
            for curValue in column:
                for char in self.values:
                    if curValue is char:
                        for target in self.targets:
                            #print target, data[i][-1]
                            if target == data[i][-1]:
                                #print "am i here?"
                                # TODO: do smoothing
                                self.demrepubHash[(target, self.attributes[i], char)] += 1
                        #if self.demrepubHash[(target, self.attributes[i], char)] is 0:
            #print target, self.attributes[i], char, "------>", self.demrepubHash[(target, self.attributes[i], char)]

            i = i +1
        '''

        pprint(self.demrepubHash)
    # Add your code here.
    # Read training data and build your naive bayes classifier
    # Store the classifier in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'
    def learn(self, train_data):
        with open(train_data, "r") as f:
            data = f.read().splitlines()

        dataList = []
        for row in data:
            instance = row.split()
            target =  instance[0]
            dataList = instance[1].split(',')
            dataList.append(target)
            self.data.append(dataList)

        self.buildHashMap(self.data)
        return;

    # Add your code here.
    # Use the learned naive bayes classifier to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'republican'
    def solve(self, query):
        inList = query.split(',')
        probDemRepub = dict ()
        for target in self.targets:
            probDemRepub[target] = float(1)

        for i, attribute in zip(range(len(inList)), self.attributes):
            for target in self.targets:

                denominator = 0
                for char in self.values:
                    denominator = denominator +self.demrepubHash[(target, attribute, char)]
                #print denominator
                #print target, attribute, inList[i], "---->", self.demrepubHash[(target, attribute, inList[i])]
                if denominator is 0:
                    #print target, attribute, inList[i]
                    denominator = 1

                probDemRepub[target] = probDemRepub[target]\
                                          *(float(self.demrepubHash[(target, attribute, inList[i])]) /float(denominator))

            #print "DemRepub: ", probDemRepub[target]

        #print probDemRepub
        max = -99999999
        maxTarget = 'democrat'
        for target in self.targets:
            if probDemRepub[target] > max:
                max = probDemRepub[target]
                maxTarget = target

        #print maxTarget
        return maxTarget