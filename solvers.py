import random
import time
import string

class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn
        
        # You should keep updating following variable with best string so far.
        self.best_state = None  
        self.counter = 0
        # self.conf_matrix_inv = conf_matrix
        self.conf_matrix_inv={}
        for i in string.ascii_lowercase:
            self.conf_matrix_inv[i]=[]
        for i in self.conf_matrix:
            for j in self.conf_matrix[i]:
                self.conf_matrix_inv[j].append(i)
        # print(self.conf_matrix_inv)

# -------------------------------------------------------------------------------------------------------------------
    def singular_change_exhaustive(self,mylist,init_list,Word_changed,start):

        self.counter += 1
        for i in range(len(mylist)):

            temp_2 = mylist[i]

            for j in range(len(temp_2)):

                temp = init_list[i]
                ch = temp[j]

                # print(temp, self.cost_fn(temp))
                for k in self.conf_matrix_inv[ch]:

                    temp = init_list[i]
                    v = [chars for chars in temp]
                    v[j] = k
                    temp = ""
                    for chars in v:
                        temp += chars

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
        print("COMPLETED1",round(time.time()-start,6),": Sentence No :",self.counter)
# ----------------------------------------------------------------------------------------------------------------------
    def singular_change_complete(self,mylist,init_list,Word_changed,start):

        for i in range(len(mylist)):

            temp = mylist[i]
            for j in range(len(temp)):

                temp = init_list[i]
                ch = temp[j]
                # print(temp, self.cost_fn(temp))
                for k in self.conf_matrix_inv[ch]:

                    temp = init_list[i]

                    v = [chars for chars in temp]
                    v[j] = k
                    temp = ""
                    for chars in v:
                        temp += chars

                    temp2 = mylist[i]

                    c1 = self.cost_fn(" ".join(mylist)) 
                    mylist[i] = temp
                    c2 = self.cost_fn(" ".join(mylist)) 
                    mylist[i] = temp2 

                    if(c2 < c1):
                        print("Changed 2",init_list[i],"->",temp)
                        mylist[i] = temp

        self.best_state = " ".join(mylist)
        print("COMPLETED2",round(time.time()-start,6))
# ----------------------------------------------------------------------------------------------------------------------
    def double_change_exhaustive(self,mylist,init_list,Word_changed,start):

        for i in range(len(mylist)):
            
            temp = init_list[i]

            # for j in range(len(temp)):
            # for j in range((len(temp)*len(temp))//2):

            
                # i1 = random.randint(0,len(temp)-1)
                # i2 = random.randint(0,len(temp)-1)
                # while(i1 == i2):
                #     i2 = random.randint(0,len(temp)-1)

                # j1 = max(i1,i2)
                # j2 = min(i1,i2)

            for j1 in range(0,len(temp)):
                for j2 in range(j1,len(temp)):

                    temp = init_list[i]

                    ch1 = temp[j1]
                    ch2 = temp[j2]
                    # print(temp, self.cost_fn(temp))
                    for k1 in self.conf_matrix_inv[ch1]:
                        for k2 in self.conf_matrix_inv[ch2]:

                            temp = init_list[i]
                            temp = init_list[i]
                            v = [chars for chars in temp]
                            v[j1] = k1
                            v[j2] = k2
                            temp = ""
                            for chars in v:
                                temp += chars

                            # print("Temp is",temp,"===",mylist[i])

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

                                if(c1 < c2):
                                    print("Changed 3:",init_list[i],"->",temp)
                                    mylist[i] = temp
                                    Word_changed[i] = True
                                    self.best_state = " ".join(mylist)

        print("COMPLETED3",round(time.time()-start,6))
# ---------------------------------------------------------------------------------------------------------------------
    def triple_change_random(self,mylist,init_list,Word_changed,start):

        for steps in range(len(mylist)):

            i = random.randint(0,len(mylist) - 1)
            temp = init_list[i]

            if(not Word_changed[i] and len(temp) >= 5):

                for j in range(len(temp)*3):

                    temp = init_list[i]

                    i1 = random.randint(0,len(temp)-1)
                    i2 = random.randint(0,len(temp)-1)
                    i3 = random.randint(0,len(temp)-1)

                    while(i1 == i2):
                        i2 = random.randint(0,len(temp)-1)
                    while(i1 == i3 or i2 == i3):
                        i3 = random.randint(0,len(temp)-1)

                    newlist = [i1,i2,i3]
                    newlist.sort()

                    j1 = newlist[0]
                    j2 = newlist[1]
                    j3 = newlist[2]

                    ch1 = temp[j1]
                    ch2 = temp[j2]
                    ch3 = temp[j3]

                    flag1 = True
                    flag2 = True
                    flag3 = True
                    # print(temp, self.cost_fn(temp))
                    for k1 in self.conf_matrix_inv[ch1]:
                        if flag1 == True:

                            for k2 in self.conf_matrix_inv[ch2]:
                                if flag2 == True :

                                    for k3 in self.conf_matrix_inv[ch3]:

                                        temp = init_list[i]
                                        v = [chars for chars in temp]
                                        v[j1] = k1
                                        v[j2] = k2
                                        v[j3] = k3
                                        temp = ""
                                        for chars in v:
                                            temp += chars

                                        temp2 = mylist[i]

                                        mylist[i] = temp
                                        c1_b = self.cost_fn(" ".join(mylist))
                                        mylist[i] = temp2
                                        c2_b = self.cost_fn(" ".join(mylist))

                                        if(c1_b > c2_b):
                                            continue

                                        else :
                                            print("Temp is",temp,"===",mylist[i])
                                            
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
                                                Word_changed[i] = True
                                                flag1 = False
                                                flag2 = False
                                                flag3 = False
                                                self.best_state = " ".join(mylist)
                                                break
                                else:
                                    break
                        else:
                            break

        print("COMPLETED4",round(time.time()-start,6))
# -----------------------------------------------------------------------------------------------------------------------------------------------------
    def quadruple_change_random(self,mylist,init_list,Word_changed,start):

        for steps in range(len(mylist)):

            i=random.randint(0,len(init_list)-1)      
            temp = init_list[i]

            if(not Word_changed[i] and len(temp) >= 7):

                for j in range(len(temp)):

                    temp = init_list[i]

                    i1 = random.randint(0,len(temp)-1)
                    i2 = random.randint(0,len(temp)-1)
                    i3 = random.randint(0,len(temp)-1)
                    i4 = random.randint(0,len(temp)-1)

                    while(i1 == i2):
                        i2 = random.randint(0,len(temp)-1)
                    while(i2 == i3 or i1==i3):
                        i3 = random.randint(0,len(temp)-1)
                    while(i1==i4 or i2==i4 or i3==i4):
                        i4 = random.randint(0,len(temp)-1)

                    newlist = [i1,i2,i3,i4]
                    newlist.sort()

                    j1 = newlist[0]
                    j2 = newlist[1]
                    j3 = newlist[2]
                    j4 = newlist[3]

                    ch1 = temp[j1]
                    ch2 = temp[j2]
                    ch3 = temp[j3]
                    ch4 = temp[j4]

                    flag1 = True
                    flag2 = True
                    flag3 = True
                    flag4 = True
                    # print(temp, self.cost_fn(temp))
                    for k1 in self.conf_matrix_inv[ch1]:
                        if flag1 == True:

                            for k2 in self.conf_matrix_inv[ch2]:
                                if flag2 == True :

                                    for k3 in self.conf_matrix_inv[ch3]:
                                        if flag3==False:
                                            break
                                        
                                        for k4 in self.conf_matrix_inv[ch4]:

                                            temp = init_list[i]
                                            v = [chars for chars in temp]
                                            v[j1] = k1
                                            v[j2] = k2
                                            v[j3] = k3
                                            v[j4] = k4
                                            temp = ""
                                            for chars in v:
                                                temp += chars

                                            temp2 = mylist[i]

                                            mylist[i] = temp
                                            c1_b = self.cost_fn(" ".join(mylist))
                                            mylist[i] = temp2
                                            c2_b = self.cost_fn(" ".join(mylist))

                                            if(c1_b > c2_b):
                                                continue

                                            else :
                                                # print("Temp is",temp,"===",mylist[i])
                                                
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
                                                    print("Changed 5:",init_list[i],"->",temp)
                                                    mylist[i] = temp
                                                    Word_changed[i] = True
                                                    flag1 = False
                                                    flag2 = False
                                                    flag3 = False
                                                    self.best_state = " ".join(mylist)
                                                    break
                                else:
                                    break
                        else:
                            break

        print("COMPLETED5",round(time.time()-start,6))
# -----------------------------------------------------------------------------------------------------------------------------------------------------
    def final_info(self,mylist,init_list,Word_changed,start):

        # self.best_state = start_state
        # print("Final Sentence :",self.best_state)
        print("Final Cost :", self.cost_fn(self.best_state))
        end = time.time()
        print("Total time taken is:",round(end - start,4),"secs","\n")
        # raise Exception("Not Implemented.")
#------------------------------------------------------------------------------------------------------------------------
    def search(self, start_state):
    
        # f = open(helper_words)

        start = time.time()

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

        no_of_random_iterations = 1

        self.singular_change_exhaustive(mylist,init_list,Word_changed,start)
        self.singular_change_complete(mylist,init_list,Word_changed,start)
        self.double_change_exhaustive(mylist,init_list,Word_changed,start)

        for random_iterations in range(no_of_random_iterations):
            self.triple_change_random(mylist,init_list,Word_changed,start)
            self.triple_change_random(mylist,init_list,Word_changed,start)
            self.triple_change_random(mylist,init_list,Word_changed,start)
            self.quadruple_change_random(mylist,init_list,Word_changed,start)

        self.final_info(mylist,init_list,Word_changed,start)

