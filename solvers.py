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
        print("Initial Sentence :",self.best_state)
        print("Initial Cost :", self.cost_fn(self.best_state))

        mylist = start_state.split(" ")
        for i in range(len(mylist)):
            temp = mylist[i]
            for j in range(len(temp)):
                ch = temp[j]
                temp = temp[:j] + ch + temp[j+1:]
                # print(temp, self.cost_fn(temp))
                for k in self.conf_matrix.keys():
                    if(ch in self.conf_matrix[k]):
                # for k in self.conf_matrix[ch]:
                        temp = temp[:j] + k + temp[j+1:]
                        
                        if(i != 0 and i != len(mylist) - 1):
                            if(self.cost_fn(mylist[i-1] +" "+ temp + " "+ mylist[i+1]) < self.cost_fn(mylist[i-1] +" "+ mylist[i] +" "+ mylist[i+1])):
                                mylist[i] = temp
                                self.best_state = " ".join(mylist)
                            else:
                                temp = temp[:j] + ch + temp[j+1:]
                            # print(mylist[i-1] + temp + mylist[i+1], self.cost_fn(temp))
                        elif(i == 0):
                            if(self.cost_fn(temp +" "+ mylist[i+1] +" "+ mylist[i+2]) < self.cost_fn(mylist[i] +" "+ mylist[i+1] +" "+ mylist[i+2])):
                                mylist[i] = temp
                                self.best_state = " ".join(mylist)
                            else:
                                temp = temp[:j] + ch + temp[j+1:]
                        else :
                            if(self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ temp ) < self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ mylist[i])):
                                mylist[i] = temp
                                self.best_state = " ".join(mylist)
                            else:
                                temp = temp[:j] + ch + temp[j+1:]
                        # print(temp)




        # self.best_state = start_state
        print("Final Sentence :",self.best_state)
        print("Final Cost :", self.cost_fn(self.best_state))
        # raise Exception("Not Implemented.")
