import pandas as pd
import numpy as np
df = pd.DataFrame([('bird', 'Falconiformes', 389.0),
                    ('bird', 'Psittaciformes', 24.0),
                    ('mammal', 'Carnivora', 80.2),
                    ('mammal', 'Primates', np.nan),
                    ('mammal', 'Carnivora', 58)],
                   index=['falcon', 'parrot', 'lion', 'monkey', 'leopard'],
                   columns=('class', 'order', 'max_speed'))
 

print(df, '\n','\n')

def printGroup(grouped_df):
    for key, item in grouped_df:
        #print(grouped_df.get_group(key), "\n\n")
        print (key, '\n','\n', item,'\n','\n','\n')
    print('exited loop')
# default is axis=0
grouped = df.groupby('class')
print(grouped.describe())
'''
printGroup(grouped)
grouped = df.groupby('order', axis='columns')
#print(type(grouped[0]))
printGroup(grouped)
grouped = df.groupby(['class', 'order'])
printGroup(grouped)
'''
