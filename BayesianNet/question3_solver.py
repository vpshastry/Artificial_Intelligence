#from pprint import pprint
class Question3_Solver:
    def __init__(self, cpt):
        # To store first order function
        self.first_table = dict()

        # To store second order function
        self.second_table = dict()

        self.cpt = cpt

        # Letters to build the first and second order functions
        self.letters = ['`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        # Letters without '`'
        self.letters_main = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        # Build both the tables
        self.build_first_table()
        self.build_second_table()

        # Helpful for examining the table, avoid otherwise
        #pprint(self.first_table)
        #pprint(self.second_table)

    # Build such that, if the query is "d-_e"
    # self.opt.conditional_prob('d', '`') *
    # self.first_table[(MissinLet, 'd')] *
    # self.opt.conditional_prob('e', MissinLet) *
    # self.opt.conditional_prob('`', 'e')
    def build_first_table(self):

        # Build 2 dimensional table with len(letters) * len(letters)
        for X in self.letters:
            for Y in self.letters:
                summation = 0
                # Hid is the hidden variable in consideration
                for hid in self.letters_main:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.cpt.conditional_prob(hid, Y))

                # Add it to the table
                self.first_table[(X, Y)] = summation

    def build_second_table(self):

        # Build 2 dimensional table with len(letters) * len(letters)
        for X in self.letters:
            for Y in self.letters:
                summation = 0
                # Hid is the hidden variable in consideration
                for hid in self.letters_main:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.first_table[(hid, Y)])

                # Add it to the table
                self.second_table[(X,Y)] = summation

    # Given the query and letter gets the conditional probability of the letter placed @underscore with the previous non-hidden variable
    def getPrevProb(self, query, let):
        underScoreIdx = query.index ('_');

        # Determine which table to use.
        if query[underScoreIdx-1] == '-':
            if query[underScoreIdx-2] == '-':
                prev = query[underScoreIdx-3];
                return self.second_table[(let, prev)]

            prev = query[underScoreIdx-2];
            return self.first_table[(let, prev)]

        prev = query[underScoreIdx-1];
        return self.cpt.conditional_prob(let, prev);

        return 1;


    # Given the query and letter gets the conditional probability of the letter placed @underscore with the next non-hidden variable
    def getPostProb(self, query, let):
        underScoreIdx = query.index ('_');

        # Determine which table to use.
        if query[underScoreIdx+1] == '-':
            if query[underScoreIdx+2] == '-':
                post = query[underScoreIdx+3];
                return self.second_table[(post, let)]

            post = query[underScoreIdx+2];
            return self.first_table[(post, let)]

        post = query[underScoreIdx+1];
        return self.cpt.conditional_prob(post, let);

    # Given the query and letter gets the conditional probability of the letter placed @underscore with the next non-hidden variable
    #    * multiplied by the conditional probability of the letter placed @underscore with the previous non-hidden variable
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
    #    query: "qu--_--n";
    #    return "t";
    def solve(self, query):
        pr_max = -999999;
        final_letter = '0';
        query = '`' + query + '`';

        # Loop over all the letters and determine the max prob
        for let in self.letters_main:
            pr_prod = self.getProb (query, let);

            # If current output is stronger(maximum) than pr_max, bow and accept him.
            if pr_prod > pr_max:
                pr_max = pr_prod;
                final_letter = let;

        return final_letter
