import random
import string

class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn
        
        # You should keep updating following variable with best string so far.
        self.best_state = None  
        self.conf_matrix_inv={}
        for i in string.ascii_lowercase:
            self.conf_matrix_inv[i]=[]
        for i in self.conf_matrix:
            for j in self.conf_matrix[i]:
                self.conf_matrix_inv[j].append(i)
        print(self.conf_matrix_inv)



    def search(self, start_state):

        # f = open(helper_words)

        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        self.best_state = start_state
        # print("Initial Sentence :",self.best_state)
        print("Initial Cost :", self.cost_fn(self.best_state))

        mylist = start_state.split(" ")
        init_list = start_state.split(" ")

        Word_changed = {}
        for i in range(len(mylist)):
            Word_changed[i] = False

# ----------------------------------------------------------------------------------------------

        for i in range(len(mylist)):

            temp_2 = mylist[i]

            for j in range(len(temp_2)):

                temp = init_list[i]
                ch = temp[j]

                # print(temp, self.cost_fn(temp))
                for k in self.conf_matrix.keys():

                    temp = init_list[i]

                    if(ch in self.conf_matrix[k]):

                        temp = temp[:j] + k + temp[j+1:]

                        # temp2 = mylist[i]

                        # mylist[i] = temp
                        # c1_b = self.cost_fn(" ".join(mylist))
                        # mylist[i] = temp2
                        # c2_b = self.cost_fn(" ".join(mylist))

                        # if(c1_b > c2_b):
                        #     continue

                        # else :
                        if(i != 0 and i != len(mylist) - 1):
                            c1 = self.cost_fn(mylist[i-1] +" "+ temp + " "+ mylist[i+1]) 
                            c2 = self.cost_fn(mylist[i-1] +" "+ mylist[i] +" "+ mylist[i+1])
                            # print(mylist[i-1] + temp + mylist[i+1], self.cost_fn(temp))
                        elif(i == 0):
                            c1 = self.cost_fn(temp +" "+ mylist[i+1] +" "+ mylist[i+2]) 
                            c2 = self.cost_fn(mylist[i] +" "+ mylist[i+1] +" "+ mylist[i+2])
                        else :
                            c1 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ temp) 
                            c2 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ mylist[i])

                        if(c1 < c2):
                            print("Changed 1:",init_list[i],"->",temp)
                            mylist[i] = temp
                            # Word_changed[i] = True
                            self.best_state = " ".join(mylist)
                        else:
                            temp = temp[:j] + ch + temp[j+1:]
                        # print(temp)

        print("COMPLETED1")

# ----------------------------------------------------------------------------------------------------------------------

        for i in range(len(mylist)):

            temp = mylist[i]
            for j in range(len(temp)):

                ch = temp[j]
                temp = temp[:j] + ch + temp[j+1:]
                # print(temp, self.cost_fn(temp))
                for k in self.conf_matrix.keys():

                    temp = init_list[i]

                    if(ch in self.conf_matrix[k]):

                        temp = temp[:j] + k + temp[j+1:]
                        temp2 = mylist[i]

                        c1 = self.cost_fn(" ".join(mylist)) 
                        mylist[i] = temp
                        c2 = self.cost_fn(" ".join(mylist)) 
                        mylist[i] = temp2 

                        if(c2 < c1):
                            print("Changed 2",init_list[i],"->",temp)
                            mylist[i] = temp
                            # Word_changed[i] = True
                            self.best_state = " ".join(mylist)
        #                 # print(temp)

# ----------------------------------------------------------------------------------------------------------------------

        for i in range(len(mylist)):
            
            temp = init_list[i]

            for j in range((len(temp)*len(temp))//3):

                temp = init_list[i]
                i1 = random.randint(0,len(temp)-1)
                i2 = random.randint(0,len(temp)-1)
                while(i1 != i2):
                    i2 = random.randint(0,len(temp)-1)

                j1 = max(i1,i2)
                j2 = min(i1,i2)

                ch1 = temp[j1]
                ch2 = temp[j2]
                # print(temp, self.cost_fn(temp))
                for k1 in self.conf_matrix.keys():
                    for k2 in self.conf_matrix.keys():

                        if(ch1 in self.conf_matrix[k1] and ch2 in self.conf_matrix[k2]):
                            temp = (temp[:j1] + k1 + temp[j1+1:j2] + k2 + temp[j2+1:])[:len(temp)]
                            # print("Temp is",temp)
                            temp2 = mylist[i]

                            mylist[i] = temp
                            c1_b = self.cost_fn(" ".join(mylist))
                            mylist[i] = temp2
                            c2_b = self.cost_fn(" ".join(mylist))

                            if(c1_b > c2_b):
                                continue

                            else :
                                if(i != 0 and i != len(mylist) - 1):
                                    c1 = self.cost_fn(mylist[i-1] +" "+ temp + " "+ mylist[i+1]) 
                                    c2 = self.cost_fn(mylist[i-1] +" "+ mylist[i] +" "+ mylist[i+1])

                                    # print(mylist[i-1] + temp + mylist[i+1], self.cost_fn(temp))
                                elif(i == 0):
                                    c1 = self.cost_fn(temp +" "+ mylist[i+1] +" "+ mylist[i+2]) 
                                    c2 = self.cost_fn(mylist[i] +" "+ mylist[i+1] +" "+ mylist[i+2])
                                else :
                                    c1 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ temp) 
                                    c2 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ mylist[i])

                                if(c1 < c2 and c1_b < c2_b and not Word_changed[i]):
                                    print("Changed 3:",init_list[i],"->",temp)
                                    mylist[i] = temp
                                    # Word_changed[i] = True
                                    self.best_state = " ".join(mylist)

        print("COMPLETED3")
# ------------------------------------------------------------------------------------------------------------

        for i in range(len(mylist)):
            
            temp = init_list[i]

            for j in range(len(temp)*len(temp)):

                temp = init_list[i]
                i1 = random.randint(0,len(temp)-1)
                i2 = random.randint(i1,len(temp)-1)
                i3 = random.randint(i2,len(temp)-1)
                # while(i1 != i2):
                #     i2 = random.randint(0,len(temp)-1)
                # while(i1 != i3 and i2 != i3):
                #     i3 = random.randint(0,len(temp)-1)

                newlist = [i1,i2,i3]
                newlist.sort()

                j1 = newlist[0]
                j2 = newlist[1]
                j3 = newlist[2]

                ch1 = temp[j1]
                ch2 = temp[j2]
                ch3 = temp[j3]
                # print(temp, self.cost_fn(temp))
                for k1 in self.conf_matrix.keys():
                    for k2 in self.conf_matrix.keys():
                        for k3 in self.conf_matrix.keys():

                            if(ch1 in self.conf_matrix[k1] and ch2 in self.conf_matrix[k2] and ch3 in self.conf_matrix[k3]):
                                temp = (temp[:j1] + k1 + temp[j1+1:j2] + k2 + temp[j2+1:j3] + k3 + temp[j3+1:])[:len(temp)]
                                # print("Temp is",temp)
                                
                                if(i != 0 and i != len(mylist) - 1):
                                    c1 = self.cost_fn(mylist[i-1] +" "+ temp + " "+ mylist[i+1]) 
                                    c2 = self.cost_fn(mylist[i-1] +" "+ mylist[i] +" "+ mylist[i+1])
                                    # print(mylist[i-1] + temp + mylist[i+1], self.cost_fn(temp))
                                elif(i == 0):
                                    c1 = self.cost_fn(temp +" "+ mylist[i+1] +" "+ mylist[i+2]) 
                                    c2 = self.cost_fn(mylist[i] +" "+ mylist[i+1] +" "+ mylist[i+2])
                                else :
                                    c1 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ temp) 
                                    c2 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ mylist[i])

                                if(c1 < c2 and not Word_changed[i]):
                                    print("Changed 4:",init_list[i],"->",temp)
                                    mylist[i] = temp
                                    # Word_changed[i] = True
                                    self.best_state = " ".join(mylist)

        print("COMPLETED4")
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------

        # self.best_state = start_state
        # print("Final Sentence :",self.best_state)
        print("Final Cost :", self.cost_fn(self.best_state),"\n")
        print()
        # raise Exception("Not Implemented.")
