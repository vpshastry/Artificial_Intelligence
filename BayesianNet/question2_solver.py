class Question2_Solver:
    def __init__(self, cpt):
        self.cpt = cpt
        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        return

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
    #    query: "que__ion";
    #    return ["s", "t"];
    def solve(self, query):
        '''#print('____________NEW____________')
        pr_max = -999999
        final_letter = '0'
        query = '`'+query+'`'
        #print(query)
        for x in self.letters:
            this_query = query.replace('_', x, 1)
            for y in self.letters:
                this_query_new = this_query.replace('_', y, 1)
                #print ('Current Guess Letters :', x, y)
                count = 0
                pr_prod = 1
                for i in this_query_new:
                    #print ('Current query letter :', i)
                    count += 1
                    if count == 1: pr_prod = pr_prod * 1
                    #elif count == len(query):
                        #pr_prod = pr_prod * 1
                    else :
                        #print('PR(', i, ',', this_query_new[count-2], ')=', self.cpt.conditional_prob(i, this_query_new[count-2]))
                        pr_prod = pr_prod * self.cpt.conditional_prob(i, this_query_new[count-2])
                #print('pr_prod for', x, y, '=', pr_prod)
                if pr_prod > pr_max:
                    pr_max = pr_prod
                    final_letter = x,y
        #print('for query=',query, 'best match was', final_letter, 'with prob', pr_max)
        return final_letter'''
        pr_max = -999999
        final_letter = '0'
        query = '`'+query+'`'
        #print(query)
        index1 = query.index('_')
        #print(index1)
        index2 = query.index('_',index1+1)
        #print(index2)
        new_query = query[index1-1:index2+2]
        #print (new_query)
        for x in self.letters:
            this_query = new_query.replace('_', x, 1)
            for y in self.letters:
                this_query_new = this_query.replace('_', y, 1)
                #print ('Current Guess Letters :', x, y)
                count = 0
                pr_prod = 1
                for i in this_query_new:
                    #print ('Current query letter :', i)
                    count += 1
                    if count >1:
                        #print('PR(', i, ',', this_query_new[count-2], ')=', self.cpt.conditional_prob(i, this_query_new[count-2]))
                        pr_prod = pr_prod * self.cpt.conditional_prob(i, this_query_new[count-2])
                #print('pr_prod for', x, y, '=', pr_prod)
                if pr_prod > pr_max:
                    pr_max = pr_prod
                    final_letter = x,y
        return final_letter
