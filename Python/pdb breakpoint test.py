a = []
 
for i in range(10):
    a.append(i)
    if i == 6:
        # Start pdb instance when i = 6
        breakpoint()
 
print(a)
