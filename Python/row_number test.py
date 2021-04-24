import pandas as pd

import numpy as np
url = ('https://raw.github.com/pandas-dev/pandas/master/pandas/tests/data/tips.csv')
tips = pd.read_csv(url)
tips.head()


tips = tips.assign(rn=tips.sort_values(['total_bill'], ascending=False))
 #  .groupby(['day'])
 #  .cumcount() + 1)
 #  .query('rn < 3')
 #  .sort_values(['day', 'rn'])
 

print(tips)
 
