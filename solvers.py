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
    def get_costs(self,mylist,i,temp):

        if(i != 0 and i != len(mylist) - 1):
            c1 = self.cost_fn(mylist[i-1] +" "+ temp + " "+ mylist[i+1]) 
            c2 = self.cost_fn(mylist[i-1] +" "+ mylist[i] +" "+ mylist[i+1])
        elif(i == 0):
            c1 = self.cost_fn(temp +" "+ mylist[i+1] +" "+ mylist[i+2]) 
            c2 = self.cost_fn(mylist[i] +" "+ mylist[i+1] +" "+ mylist[i+2])
        else :
            c1 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ temp) 
            c2 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ mylist[i])

        return (c1,c2)
#---------------------------------------------------------------------------------------------------------------------
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

                    #Not checking the overall costs as this function only checks the local correctness 
                    #thus encouraging exploration through local costs.

                    c1,c2 = self.get_costs(mylist,i,temp)

                    if(c1 < c2):
                        # print("Changed 1:",init_list[i],"->",temp)
                        mylist[i] = temp
                        # Word_changed[i] = True
        self.best_state = " ".join(mylist)
        # print("COMPLETED1",round(time.time()-start,6))
# ----------------------------------------------------------------------------------------------------------------------
    def singular_change_complete(self,mylist,init_list,Word_changed,start):

        for i in range(len(mylist)):

            temp = init_list[i]

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
                        # print("Changed 2",init_list[i],"->",temp)
                        mylist[i] = temp

            c1 = self.cost_fn(" ".join(mylist)) 
            temp2 = mylist[i]
            temp = init_list[i]
            mylist[i] = temp
            c2 = self.cost_fn(" ".join(mylist)) 
            if(c2 < c1):
                # print("Changed 2",init_list[i],"->",temp)
                mylist[i] = temp

        self.best_state = " ".join(mylist)
        # print("COMPLETED2",round(time.time()-start,6))
# ----------------------------------------------------------------------------------------------------------------------
    def double_change_exhaustive(self,mylist,init_list,Word_changed,start):

        for i in range(len(mylist)):
            
            temp = init_list[i]

            for j1 in range(0,len(temp)):
                for j2 in range(j1,len(temp)):

                    temp = init_list[i]

                    ch1 = temp[j1]
                    ch2 = temp[j2]

                    for k1 in self.conf_matrix_inv[ch1]: #Exhaustive depth first search for each word of the sentence
                        for k2 in self.conf_matrix_inv[ch2]: #along with storing the best optimal solution similar to local search

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

                                c1,c2 = self.get_costs(mylist,i,temp)

                                if(c1 < c2):
                                    # print("Changed 3:",init_list[i],"->",temp)
                                    mylist[i] = temp
                                    Word_changed[i] = True
                                    self.best_state = " ".join(mylist)

        # print("COMPLETED3",round(time.time()-start,6))
# -----------------------------------------------------------------------------------------------------------------------------------------------------
    def update_costs(self,mylist,n):
        costs=[]
        for i in range(len(mylist)):
            if(len(mylist[i])>=n):
                if(i > 1 and i < len(mylist) - 2):
                    c1 = self.cost_fn(mylist[i-1] +" "+ mylist[i] + " "+ mylist[i+1])
                    c2 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] + " "+ mylist[i])
                    c3 = self.cost_fn(mylist[i] +" "+ mylist[i+1] + " "+ mylist[i+2])
                    costs.append((i,c1+c2+c3))
                elif(i == 0):
                    c1 = self.cost_fn(mylist[i] +" "+ mylist[i+1] +" "+ mylist[i+2]) 
                    costs.append((i,c1*2.5))
                else:
                    c1 = self.cost_fn(mylist[i-2] +" "+ mylist[i-1] +" "+ mylist[i]) 
                    costs.append((i,c1*2.5))

        costs.sort(key=lambda x:x[1],reverse=True)
        return costs
# ---------------------------------------------------------------------------------------------------------------------
    def triple_quad_change_random(self,mylist,init_list,Word_changed,start):
        
        costs=self.update_costs(mylist,5)
    
        p = 0

        while p < len(costs):
            # print("p =",p)
            i = costs[p][0]
            temp = init_list[i]
            c=10

            if(not Word_changed[i]):
                # print("In loop 3",init_list[i],mylist[i]) 
                flag0 = True
                
                for j in range(len(temp)*c):
                    if flag0 :

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
                        flag4 = True

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
                                                # p += 1
                                                continue

                                            else :
                                                # print("Temp is",temp,"===",mylist[i])
                                                
                                                c1,c2 = self.get_costs(mylist,i,temp)

                                                if(c1 < c2 and not Word_changed[i]):

                                                    # print("Changed 4:",init_list[i],"->",temp)
                                                    
                                                    mylist[i] = temp
                                                    Word_changed[i] = True
                                                    flag0 = False
                                                    flag1 = False
                                                    flag2 = False
                                                    flag3 = False
                                                    flag4 = False
                                                    self.best_state = " ".join(mylist)
                                                    costs=self.update_costs(mylist,5)
                                                    p = 0
                                                # self.singular_change_complete(mylist,init_list,Word_changed,start)
                                                    break
                                    else:
                                        break
                            else:
                                break
                        # p += 1
                    else:
                        break
                        

                if flag4 and len(init_list[i])>=7 and not Word_changed[i]:
                  flag5 = True
                #   print("In loop 4",init_list[i],mylist[i])  
                  for j in range(len(init_list[i])*10):
                    if flag5 == False:
                        break

                    temp = init_list[i]

                    i1 = random.randint(0,len(temp)-1)
                    i2 = random.randint(0,len(temp)-1)
                    i3 = random.randint(0,len(temp)-1)
                    i4 = random.randint(0,len(temp)-1)

                    while(i1 == i2):   #implementing randomization - getting 4 random unequal indexes - non exhaustive search
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
                                                # p += 1
                                                continue

                                            else :
                                                # print("Temp is",temp,"===",mylist[i])
                                                
                                                c1,c2 = self.get_costs(mylist,i,temp)

                                                if(c1 < c2 and not Word_changed[i]):
                                                    # print("Changed 5:",init_list[i],"->",temp)
                                                    mylist[i] = temp
                                                    Word_changed[i] = True
                                                    flag1 = False
                                                    flag2 = False
                                                    flag3 = False
                                                    flag4 = False
                                                    flag5 = False
                                                    self.best_state = " ".join(mylist)
                                                    costs=self.update_costs(mylist,5)
                                                    p = 0
                                                    break
                                else:
                                    break
                        else:
                            break
                    p += 1
                elif flag4 and not (len(init_list[i])>=7 and not Word_changed[i]):
                    p += 1
            else :
                p += 1

        # print("COMPLETED4",round(time.time()-start,6))
# -----------------------------------------------------------------------------------------------------------------------------------------------------
    def penta_change_random(self,mylist,init_list,Word_changed,start):

        costs=self.update_costs(mylist,9)
    
        p = 0
        
        while p < len(costs):

            # print("p =",p)
            i = costs[p][0]
            temp = init_list[i]
            
            if(not Word_changed[i]):

                for j in range(len(temp)*3):

                    temp = init_list[i]

                    i1 = random.randint(0,len(temp)-1)
                    i2 = random.randint(0,len(temp)-1)
                    i3 = random.randint(0,len(temp)-1)
                    i4 = random.randint(0,len(temp)-1)
                    i5 = random.randint(0,len(temp)-1)

                    while(i1 == i2):
                        i2 = random.randint(0,len(temp)-1)
                    while(i2 == i3 or i1==i3):
                        i3 = random.randint(0,len(temp)-1)
                    while(i1==i4 or i2==i4 or i3==i4):
                        i4 = random.randint(0,len(temp)-1)
                    while(i1==i5 or i2==i5 or i3==i5 or i4==i5):
                        i5 = random.randint(0,len(temp)-1)


                    newlist = [i1,i2,i3,i4,i5]
                    newlist.sort()

                    j1 = newlist[0]
                    j2 = newlist[1]
                    j3 = newlist[2]
                    j4 = newlist[3]
                    j5 = newlist[4]

                    ch1 = temp[j1]
                    ch2 = temp[j2]
                    ch3 = temp[j3]
                    ch4 = temp[j4]
                    ch5 = temp[j5]

                    flag1 = True
                    flag2 = True
                    flag3 = True
                    flag4 = True

                    for k1 in self.conf_matrix_inv[ch1]:
                        if flag1 == True:

                            for k2 in self.conf_matrix_inv[ch2]:
                                if flag2 == True :

                                    for k3 in self.conf_matrix_inv[ch3]:
                                        if flag3==False:
                                            break
                                        
                                        for k4 in self.conf_matrix_inv[ch4]:
                                          if flag4==False:
                                                break

                                          for k5 in self.conf_matrix_inv[ch5]:

                                            temp = init_list[i]
                                            v = [chars for chars in temp]
                                            v[j1] = k1
                                            v[j2] = k2
                                            v[j3] = k3
                                            v[j4] = k4
                                            v[j5] = k5
                                            temp = ""
                                            for chars in v:
                                                temp += chars

                                            temp2 = mylist[i]

                                            mylist[i] = temp
                                            c1_b = self.cost_fn(" ".join(mylist))
                                            mylist[i] = temp2
                                            c2_b = self.cost_fn(" ".join(mylist))

                                            if(c1_b > c2_b):
                                                # p += 1
                                                continue

                                            else :
                                                # print("Temp is",temp,"===",mylist[i])
                                                
                                                c1,c2 = self.get_costs(mylist,i,temp)

                                                if(c1 < c2 and not Word_changed[i]):
                                                    # print("Changed 5:",init_list[i],"->",temp)
                                                    mylist[i] = temp
                                                    Word_changed[i] = True
                                                    flag1 = False
                                                    flag2 = False
                                                    flag3 = False
                                                    flag4 = False
                                                    costs=self.update_costs(mylist,9)
                                                    self.best_state = " ".join(mylist)
                                                    p=0
                                                    break
                                else:
                                    break
                        else:
                            break
                    p += 1
            else:
                p += 1

        # print("COMPLETED7",round(time.time()-start,6))
# ----------------------------------------------------------------------------------------------------------------------
    def backtrack_change(self,mylist,init_list,Word_changed,start):

        for i in range(len(mylist)): #backtracking the changed words, incase a word has been mistakenly replaced 
                                     #due to local optimization
            temp = init_list[i]
            temp2 = mylist[i]

            c1 = self.cost_fn(" ".join(mylist)) 
            mylist[i] = temp
            c2 = self.cost_fn(" ".join(mylist)) 
            mylist[i] = temp2 

            if(c2 < c1):
                # print("Changed 6:",mylist[i],"->",temp)
                mylist[i] = temp
                self.best_state = " ".join(mylist)

        # print("COMPLETED6",round(time.time()-start,6))
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
    
        start = time.time()

        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        self.best_state = start_state
        # print("Initial Sentence :",self.best_state)
        # print("Initial Cost :", self.cost_fn(self.best_state))

        mylist = start_state.split(" ")
        init_list = start_state.split(" ")

        Word_changed = {}
        for i in range(len(mylist)):
            Word_changed[i] = False

        no_of_random_iterations = 100 #Can be fine tuned, given the time available

        self.singular_change_exhaustive(mylist,init_list,Word_changed,start) #Single level local cost DFS on each word and local updation
        self.singular_change_complete(mylist,init_list,Word_changed,start)   #Single level overall cost DFS on each word and local updation
        self.double_change_exhaustive(mylist,init_list,Word_changed,start)   #Level 2 DFS on each word, exhaustive and local updation
        self.singular_change_exhaustive(mylist,init_list,Word_changed,start) #Single level local cost DFS on each word and local updation, after a level 2 DFS updation has taken place
        self.backtrack_change(mylist,init_list,Word_changed,start)           #Backtracking the changes made to sentences due to local cost DFS

        for random_iterations in range(no_of_random_iterations):
            self.triple_quad_change_random(mylist,init_list,Word_changed,start)   #Non exhaustive, random, Level 3 and Level 4 local DFS on the worst words that occurs in the sentence, local updation
            self.triple_quad_change_random(mylist,init_list,Word_changed,start)   #Non exhaustive, random, Level 3 and Level 4 local DFS on the worst words that occurs in the sentence, local updation, a 2nd time in case due to randomness the errors were not removed
            self.triple_quad_change_random(mylist,init_list,Word_changed,start)   #Non exhaustive, random, Level 3 and Level 4 local DFS on the worst words that occurs in the sentence, local updation, a 3rd time in case due to randomness the errors were not removed
            self.penta_change_random(mylist,init_list,Word_changed,start)         #Non exhaustive, random, Level 5 DFS on the worst words that occurs in the sentence found greedily
            for i in range(len(mylist)):
                Word_changed[i] = False
        # self.final_info(mylist,init_list,Word_changed,start) #Printing the final info - the final cost of the output sentence, and the total time taken by the algorithm

