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
                          'duty-free-exports', 'export-administration-act-south-africa', 'class', 'null']
        self.learn('train.data')
        return;

    def buildHashMap(self, data):
        for target in self.targets:
            for char in self.values:
                for curAttribute in self.attributes:
                    self.demrepubHash[(target, curAttribute, char)] = 0

        i = 0

        for column in zip(*data):
            for curValue in column:
                for char in self.values:
                    if curValue is char:
                        for target in self.targets:
                            # TODO: do smoothing
                            self.demrepubHash[(target, self.attributes[i], char)] += 1
                        #if self.demrepubHash[(target, self.attributes[i], char)] is 0:
            #print target, self.attributes[i], char, "------>", self.demrepubHash[(target, self.attributes[i], char)]

            i = i +1

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

        for target in self.targets:
            for i, attribute in zip(range(len(inList)), self.attributes):
                denominator = 0
                for char in self.values:
                    denominator = denominator +self.demrepubHash[(target, attribute, char)]
                #print denominator
                #print self.demrepubHash[(target, attribute, inList[i])]

                probDemRepub[target] = probDemRepub[target]\
                                          *(float(self.demrepubHash[(target, attribute, inList[i])]) /float(denominator))

            print "DemRepub: ", probDemRepub[target]

        max = -99999999
        maxTarget = 'democrat'
        for target in self.targets:
            if probDemRepub[target] > max:
                max = probDemRepub[target]
                maxTarget = target

        return maxTarget