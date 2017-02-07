
# coding: utf-8

# In[105]:

import pandas as pd
import numpy as np
import zipfile, requests, io


# In[106]:

""" modes function for table """

def mod_table(df) :
    modes = df.mode()
    return modes


# In[107]:

""" read data URL """

path = "http://archive.ics.uci.edu/ml/machine-learning-databases/00368/Facebook_metrics.zip"

r = requests.get(path, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
file = z.extract('dataset_Facebook.csv')

data = pd.read_csv(file, sep = ';')

""" drop rows with NaN values """

data = data.dropna(0, how = 'any')


# In[108]:

""" mean, max, min, median and mode for all data """

for col in list(data) :
    print(col, 'modes', data[col].mode(), "\n")

data.describe()


# In[109]:

""" mode for each types """

modes = pd.DataFrame(data.groupby('Type').apply(mod_table)).fillna("")
modes


# In[67]:

""" mean, max, min, median for each types """

data.groupby('Type').describe()


# In[104]:

""" the most popular """

dplc = data.duplicated()
print(dplc.unique())


# In[ ]:

""" there aren't any duplicate rows at data table, so all objects in set are unique (there isn't popular object)"""

