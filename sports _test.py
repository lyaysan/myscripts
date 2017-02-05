
# coding: utf-8

# In[302]:

import pandas as pd
import numpy as np
import seaborn
get_ipython().magic('matplotlib inline')


# In[270]:

""" modes function for column """

def mod_column(df, column) :
    modes = df[column].mode()
    if modes.count() == 0 :
        print("nothing has 2+ occurrences")
    return modes


# In[271]:

""" modes function for table """

def mod_table(df) :
    modes = df.mode()
    #if modes.count() == 0 :
    #    print("nothing has 2+ occurrences")
    return modes


# In[288]:

""" generate random data """

dates = pd.date_range('20170101', '20171231', freq = 'W-MON')
rdata = pd.DataFrame(np.random.randn(np.size(dates),4), index=dates, columns=['par1', 'par2', 'par3', 'par4'])
rdata['type'] = [chr(np.random.random_integers(65, 67)) for i in dates]
rdata.head(10)


# In[289]:

""" mean, max, min, median and mode for the table """

print("mean", rdata.select_dtypes(exclude = ['object']).unstack().mean())
print("maximum", rdata.select_dtypes(exclude = ['object']).unstack().max())
print("minimum", rdata.select_dtypes(exclude = ['object']).unstack().min())
print("median", rdata.select_dtypes(exclude = ['object']).unstack().median())
print("modes", rdata.select_dtypes(exclude = ['object']).unstack().mode())


# In[290]:

""" mean, max, min, median and mode for the each column """

for col in list(rdata) :
    print(col)
    print("modes\n", mod_column(rdata, col))
rdata.describe()


# In[291]:

""" mean, max, min, median and mode for the each column for each types"""

print(rdata.groupby('type').apply(mod_table))

rdata.groupby('type').describe()


# In[301]:

""" visualization """

rdata.groupby('type').hist()

