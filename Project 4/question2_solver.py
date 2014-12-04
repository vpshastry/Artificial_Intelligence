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
            j = 0
            for char in column:
                if char == self.targets[0] or char == self.targets[1]:
                    continue

                self.demrepubHash[(data[j][-1], self.attributes[i], char)] += 1
                j += 1

            i += 1

        return

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

                probDemRepub[target] = probDemRepub[target]\
                                          *(float(self.demrepubHash[(target, attribute, inList[i])]) /float(denominator))


        max = -99999999
        maxTarget = 'democrat'
        for target in self.targets:
            if probDemRepub[target] > max:
                max = probDemRepub[target]
                maxTarget = target

        return maxTarget