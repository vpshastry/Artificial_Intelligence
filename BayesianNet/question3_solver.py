class Question3_Solver:
    def __init__(self, cpt):
        self.first_table = dict()
        self.second_table = dict()
        self.cpt = cpt
        self.letters = ['`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.build_first_table()
        self.build_second_table()

    def build_first_table(self):
        summation = 0
        for X in self.letters:
            for Y in self.letters:
                for hid in self.letters:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.cpt.conditional_prob(hid, Y));

                self.first_table[(X,Y)] = summation

    #def getfirsttab(X, Y):
        #return self.firsttab[self.letters.index[X]][self.letters.index[Y]];

    def build_second_table(self):
        summation = 0
        for X in self.letters:
            for Y in self.letters:
                for hid in self.letters:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.first_table[(hid,Y)]);
                    #print(X,Y,hid)
                self.second_table[(X,Y)] = summation

    #def getsecondtab(X, Y):
        #return self.secondtab[self.letters.index[X]][self.letters.index[Y]];

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
    #    query: "qu--_--n";
    #    return "t";
    def solve(self, query):
        return "t";

