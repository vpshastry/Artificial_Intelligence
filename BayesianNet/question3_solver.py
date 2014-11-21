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
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.cpt.conditional_prob(hid, Y))
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
        pr_max = -999999
        final_letter = '0'
        query = '`'+query+'`'

        for i in self.letters:
            this_query = query.replace ('_', i);

            count = 0;
            pr_prod = 1;
            func = 0;

            for j in this_query:
                if j == '-':
                    func = func +1;
                    continue;

                count += 1;
                if count == 1:
                    continue;

                if func == 0:
                    pr_prod = pr_prod * self.cpt.conditional_prob(j, this_query[count-2]);
                elif func == 1:
                    pr_prod = pr_prod * self.first_table[(j, this_query[count-3])];
                    func = 0
                elif func == 2:
                    pr_prod = pr_prod * self.second_table[(j, this_query[count-4])];
                    func = 0
                else:
                    print "ERROR............... Exiting"
                    sys.exit()


            if pr_prod > pr_max:
                pr_max = pr_prod;
                final_letter = i;

        return final_letter;

