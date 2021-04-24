bil=map(float,[939,263,590,610,614,375,591])
label=["ss","interest","defense","nondefense","other","medicaid","medicare"]
out=[]
for x in bil:
    out.append(x/sum(bil)*15163)
print (label)
print(out)
print(sum(out))
#print(out,'\n',label)
