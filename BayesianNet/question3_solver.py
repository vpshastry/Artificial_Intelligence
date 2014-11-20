class Question3_Solver:
    def __init__(self, cpt):
        self.firsttab = [[0 for k in range(27)] for i in range(27)]
        self.cpt = cpt;
        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.build_first_table();

    def build_first_table():
        sum = 0
        for X in self.letters:
            for Y in self.letters:
                for hid in self.letters:
                    summation = summation + (self.cpt.conditional_prob(X, hid) * self.cpt.conditional_prob(hid, Y));
                    print X, hid, Y

                self.firsttab[X][Y] = summation

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
        return final_letter


