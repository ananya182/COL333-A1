file1 = ".\data\pred_tc.txt"
file2 = ".\data\corpus.txt"

f = open(file1,"r")
Lines1 = f.readlines()
f.close()

f2 = open(file2,"r")
Lines2 = f2.readlines()
f.close()

count_corrected = 0

for i in range(len(Lines1)):
    if(Lines1[i] == Lines2[i]):
        count_corrected +=1
    print("Line",i+1,Lines1[i] == Lines2[i])

print("\nNo of corrected lines :",count_corrected)
print("No of uncorrected lines :",len(Lines1) - count_corrected)