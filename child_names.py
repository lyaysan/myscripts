
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().magic('matplotlib inline')


# In[2]:

#add proportions into a dataframe table GROUP

def add_prop(group):
    births = group.numbers.astype(float)
    group['prop'] = births/births.sum()
    return group


# In[3]:

#read data from https://www.ssa.gov/oact/babynames/limits.html

columns = ['name', 'gender', 'numbers']
names1880 = pd.read_csv('C:\\Users\\Dima\\Downloads\\names\\yob1880.txt', names = columns)


# In[4]:

names1880.head()


# In[5]:

names1880.groupby('gender').numbers.sum()


# In[6]:

#concatenate data from all files into single dataframe table

years = range(1880,2016)

pieces = []

for year in years :
    path = 'C:\\Users\\Dima\\Downloads\\names\\yob%d.txt' % year
    frame = pd.read_csv(path, names = columns)
    
    frame ['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index = True)


# In[7]:

#pivot table for chart

total_numbers = names.pivot_table(names, index = ['year'], columns = 'gender', aggfunc = sum)
total_numbers.head()


# In[8]:

#plotting
def plotting(data, values, x, y, c_title) :
    plt.plot(data, values)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.title(c_title)
    plt.show()
    
plt.plot(years, total_numbers['numbers']['F'], years, total_numbers['numbers']['M'])
plt.xlabel('Years')
plt.ylabel('Births')
plt.grid(True) 
plt.title('Total Births From 1880 To 2015 By Year and Gender')
plt.legend(['F', 'M'])
plt.show()


# In[9]:

names = names.groupby(['year', 'gender']).apply(add_prop)


# In[10]:

names.head()


# In[11]:

#check sum(prop) = 1 
np.allclose(names.groupby(['year','gender']).prop.sum(), 1)


# In[12]:

#collect top 1000 names for each pair (gender, year) for work

def get_top1000(group):
    return group.sort_values(by = 'numbers', ascending = False)[:1000]


# In[13]:

grouped = names.groupby(['year','gender'])
top1000 = grouped.apply(get_top1000)


# In[14]:

#split data to boys-data and gorls-data

boys = top1000[top1000.gender == 'M']
girls = top1000[top1000.gender == 'F']


# In[15]:

#group data for names

total_births = top1000.pivot_table(top1000, index = ['year'], columns = 'name', aggfunc = sum)
total_births.head()


# In[16]:

plotting(years, total_births['numbers']['John'], 'years', 'births', 'Dipper')


# In[17]:

plotting(years, total_births['numbers']['John'], 'years', 'births', 'Mabel')


# In[18]:

#name varety (how part of female names and male names changes)

table = top1000.pivot_table(top1000, index = ['year'], columns = 'gender', aggfunc = sum)
plotting(years, table['prop']['F'], 'years', 'proportions', 'part births - girls')
plotting(years, table['prop']['M'], 'years', 'proportions', 'part births - boys')


# In[19]:

table.head()


# In[20]:

#position of 50% most popular names at 2010

df2010 = boys[boys.year == 2010]
prop_cumsum = df2010.sort_values(by = 'prop', ascending = False).prop.cumsum()
prop_cumsum.searchsorted(0.5)


# In[21]:

#position of 50% most popular names at 1900

df1900 = boys[boys.year == 1900]
prop_cumsum = df1900.sort_values(by = 'prop', ascending = False).prop.cumsum()
prop_cumsum.searchsorted(0.5)


# In[22]:

def get_quantile_count(group, q = 0.5) :
    group = group.sort_values(by = 'prop', ascending = False)
    return group.prop.cumsum().searchsorted(0.5) + 1

diversity = top1000.groupby(['year', 'gender']).apply(get_quantile_count)
diversity = diversity.unstack('gender')


# In[27]:

diversity['F'].head(10)


# In[30]:

plotting(years, diversity['F'], 'year', 'names', 'number of popular female names in top 50%')


# In[29]:

plotting(years, diversity['M'], 'year', 'names', 'number of popular male names in top 50%')


# In[53]:

#last letter revolution

get_last_letter = lambda x : x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last letter'

table = names.pivot_table(names, index = last_letters, columns = ['gender', 'year'], aggfunc = sum)


# In[56]:

table.head()


# In[55]:

subtable = table.reindex(columns = [1910, 1960, 2010], level = 'year')
subtable.head()


# In[77]:

#part of names with the letter among all names for each pair gender-year

subtable.sum()


# In[78]:

letter_prop = subtable/subtable.sum().astype(float)
letter_prop['numbers'].head()


# In[71]:

fig, axes = plt.subplots(2, 1, figsize = (10, 8))
ch1 = letter_prop['numbers']['M'].plot(kind = 'bar', rot = 0, ax = axes[0], title = 'Male')
ch2 = letter_prop['numbers']['F'].plot(kind = 'bar', rot = 0, ax = axes[1], title = 'Female', legend = False)
plt.show()


# In[81]:

letter_prop = table/table.sum().astype(float)
dny_ts = letter_prop['numbers'].ix[['d', 'n', 'y'], 'M'].T
dny_ts.head()


# In[83]:

dny_ts.plot()
plt.show()


# In[85]:

# female names become male and conversely

all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])

lesley_like = all_names[mask]


# In[91]:

lesley_like 


# In[92]:

filtered = top1000[top1000.name.isin(lesley_like )]


# In[95]:

filtered.groupby('name').numbers.sum()


# In[98]:

table = filtered.pivot_table(filtered, index = 'year', columns = ['gender'], aggfunc = sum)
table = table.div(table.sum(1), axis = 0)
table['numbers'].tail()


# In[ ]:

table['numbers'].plot(style={'M': 'k-', 'F': 'k--'})
plt.show()


# In[ ]:



