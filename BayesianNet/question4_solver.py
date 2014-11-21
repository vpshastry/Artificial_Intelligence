class Question4_Solver:
    def __init__(self, cpt):
        self.first_table = dict()
        self.second_table = dict()
        self.cpt = cpt
        self.letters = ['`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.letters_main = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.build_first_table()
        self.build_second_table()
        #pprint(self.first_table)
        #pprint(self.second_table)

    def build_first_table(self):

        for X in self.letters:
            for Y in self.letters:
                summation = 0
                for hid in self.letters_main:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.cpt.conditional_prob(hid, Y))
                self.first_table[(X, Y)] = summation

    #def getfirsttab(X, Y):
        #return self.firsttab[self.letters.index[X]][self.letters.index[Y]];

    def build_second_table(self):

        for X in self.letters:
            for Y in self.letters:
                summation = 0
                for hid in self.letters_main:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.first_table[(hid, Y)])
                    #print(X,Y,hid)
                self.second_table[(X,Y)] = summation

    #####################################
    # ADD YOUR CODE HERE
    # Pr(x|y) = self.cpt.conditional_prob(x, y);
    # A word begins with "`" and ends with "`".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt.conditional_prob("a", "`") * \
    #    self.cpt.conditional_prob("b", "a") * \
    #    self.cpt.conditional_prob("`", "b");
    # query example:
    #    query: ["que-_-on", "--_--icial",
    #            "in_elligence", "inter--_"];
    #    return "t";
    def solve(self, query):
        return "t";

