class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far.
        self.best_state = None  

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        self.best_state = start_state
        print("Initial Cost :", self.cost_fn(self.best_state))

        mylist = start_state.split(" ")
        for i in range(len(mylist)):
            temp = mylist[i]
            for j in range(len(temp)):
                ch = temp[j]
                for k in self.conf_matrix[ch]:
                    temp = temp[:j] + k + temp[j+1:]
                    print(temp, self.cost_fn(temp))
                    if(self.cost_fn(temp) < self.cost_fn(mylist[i])):
                        mylist[i] = temp
                        self.best_state = " ".join(mylist)
                    else:
                        temp = temp[:j] + ch + temp[j+1:]


        # self.best_state = start_state
        print("Final Cost :", self.cost_fn(self.best_state))
        # raise Exception("Not Implemented.")
