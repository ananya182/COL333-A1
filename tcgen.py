import random
def createtc():
        a=[0,1]
        weightwords=[0.7,0.3]
        weightchar=[0.9,0.1]
        f=open("data/corpus.txt","r")
        g=open("data/tc.txt","w")
        l=f.readlines()
       # print(l)
        for i in l:
            x=i.split()
           # print(x)
            st=' '
            
            for j in range(len(x)):
                rand = random.choices(a, weights=weightwords, k=1)
                if rand[0]:
                    for k in range(len(x[j])):
                        rand = random.choices(a, weights=weightchar, k=1)
                        if rand[0]:
                           # print("j,k={}{}".format(j,k))
                            #print("x[{}][{}]=".format(j,k),x[j][k])
                            new=random.choice(self.conf_matrix[x[j][k]])
                            x[j]=x[j][:k]+new+x[j][k+1:]
            line=st.join(x)
           # print(line)
            g.write(line+'\n') 