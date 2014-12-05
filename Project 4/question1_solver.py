class Question1_Solver:
    def __init__(self):
        self.tree = dict();
        self.targets = ['democrat', 'republican']
        self.learn('train.data');
        self.attributes =['handicapped-infants', 'water-project-cost-sharing', 'adoption-of-the-budget-resolution',
                          'physician-fee-freeze', 'el-salvador-aid', 'religious-groups-in-schools',
                          'anti-satellite-test-ban', 'aid-to-nicaraguan-contras', 'mx-missile', 'immigration',
                          'synfuels-corporation-cutback', 'education-spending', 'superfund-right-to-sue', 'crime',
                          'duty-free-exports', 'export-administration-act-south-africa', 'class']
        return;

    # Add your code here.
    # Read training data and build your decision tree
    # Store the decision tree in this class
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

        self.buildTree(self.data, attribute_list, "class")
        return;

    def isAllOfSameClass(self, data):
        lclass = data[0][self.attributes.indexof ('class')]
        for tuple in data:
            if not tuple[self.attributes.indexof ('class')] is lclass:
                return None

        return lclass

    def getMajorityClass(self, data):
        counter['democrat'] = counter['republican'] = 0

        for tuples in data:
            counter[tuples[self.attributes.indexof('class')]] += 1

        if (counter[self.targets[0]] > counter[self.targets[1]]):
            return self.targets[0]
        return self.targets[1]

    def buildTree(self, data, attribute_list, inClass):
        # Create a node N

        # If tuples in D are all of the same class C then
        # return N as a leaf node labeled with the class C
        lclass = self.isAllOfSameClass(data)
        if not lclass is None:
            return {'y': lclass, 'n': lclass, '?': lclass}

        # If attribute list is empty return N as a leaf node
        # labeled with the majority class in D
        if not attribute_list:
            lclass = self.getMajorityClass(data)
            return lclass

        # Apply Attribute selection method (d, attr_list) to find the
        # best splitting criterions
        self.attributeSelectionMethod (data, attribute_list)

        #label Node N with splitting criterion

        # if splitting_attribute is discrete valued AND
        # multiway split allowed then (Not restricted to binary trees)
        # attribute list = attribute_list - splitting attribute

        # For each outcome j of splitting criterion
        # partition the tuples and grow subtrees for each partition
        # let Dj be the set of data tuples in D satisfying outcome j;

        return newTree


    # Add your code here.
    # Use the learned decision tree to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'republican'
    def solve(self, query):
        return 'democrat';

