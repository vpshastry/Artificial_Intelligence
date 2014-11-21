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

    def getPrevProb(self, query, let):
        underScoreIdx = query.index ('_');
        prevfunc = 0;

        if query[underScoreIdx-1] == '-':
            if query[underScoreIdx-2] == '-':
                prevfunc = 2;
                prev = query[underScoreIdx-3];
            else:
                prevfunc = 1;
                prev = query[underScoreIdx-2];
        else:
            prev = query[underScoreIdx-1];

        if prevfunc == 0:
            return self.cpt.conditional_prob(let, prev);
        elif prevfunc == 1:
            return self.first_table[(let, prev)]
        elif prevfunc == 2:
            return self.second_table[(let, prev)]
        else:
            #print("ERROR............... Exiting")
            exit()

        return 1;


    def getPostProb(self, query, let):
        underScoreIdx = query.index ('_');
        postfunc = 0;

        if query[underScoreIdx+1] == '-':
            if query[underScoreIdx+2] == '-':
                postfunc = 2;
                post = query[underScoreIdx+3];
            else:
                postfunc = 1;
                post = query[underScoreIdx+2];
        else:
            post = query[underScoreIdx+1];

        if postfunc == 0:
            return self.cpt.conditional_prob(post, let);
        elif postfunc == 1:
            return self.first_table[(post, let)]
        elif postfunc == 2:
            return self.second_table[(post, let)]
        else:
            #print("ERROR............... Exiting")
            exit()

        return 1;

    def getProb(self, query, let):
        return self.getPrevProb(query, let) * self.getPostProb(query, let);

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
        pr_max = -999999;
        final_letter = '0';

        for let in self.letters_main:
            pr_prod = 1;
            for qiter in query:
                qiter = '`' + qiter + '`';
                pr_prod = pr_prod * self.getProb (qiter, let);

            if pr_prod > pr_max:
                pr_max = pr_prod;
                final_letter = let;

        return final_letter
        #return "t";
