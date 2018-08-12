
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[119]:


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[120]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[121]:


species.head()


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[122]:


print("Total species count equals; " + str(species.count()))
print("Unique scientific names of species is only:" + str(species['scientific_name'].nunique()))
# There are 5824 entries in the species dataframe, but possibly only 5541 unique scientific names. 
# NOTE: It might be important to check for duplicates in the dataframe.


# What are the different values of `category` in `species`?

# In[123]:


species.category.unique()
# There are 7 unique categories


# In[124]:


species.groupby(['category']).scientific_name.count()

species_categories = species.category.unique()
species_category_count = species.groupby(['category']).scientific_name.count()

#make your pie chart here
fig, ax = plt.subplots(figsize=(14, 7), subplot_kw=dict(aspect="equal"))
plt.pie(species_category_count)
plt.pie(species_category_count,
        labels=species.category.unique(),
        autopct= '%0.1f%%',pctdistance=.8, labeldistance=1.1)

plt.title("Categories of Species",fontsize = 25)

plt.show()


# What are the different values of `conservation_status`?

# In[125]:


species.conservation_status.unique()
# There are five unique conservation status.  'nan' could indicate no concern or no data.


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[126]:


species.groupby(['conservation_status']).count()
# This is missimg all data with null values. Null values are only in conservations status. 


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[127]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Intervention`.

# In[128]:


species.groupby(['conservation_status']).count()
#This includes null values.


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[129]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')
protection_counts


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[130]:


#1 Figure Size = width 10, length 4
plt.figure(figsize=(10,4))
#2 Axes obect = ax - used for positioning labeling of x an y ticks
ax = plt.subplot()
#3 Create a bar chart - heights=scientific_name of protection_counts
plt.bar(range(len(protection_counts.scientific_name)),protection_counts.scientific_name)
#4,#5 Create x tick for each bar
cstat_labels = protection_counts.conservation_status
plt.xticks(range(len(protection_counts)),cstat_labels)
#6 label y axis
plt.ylabel('Number of Species')
#7 Title graph
plt.title('Conservation Status by Species', fontsize = 25)
#8 Plot the graph
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?
Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.
# In[131]:


species['is_protected'] = np.where(species.conservation_status != "No Intervention",'True','False')
species.head()


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[132]:


#Take into account only the unique scientific_names.
category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()


# Examine `category_count` using `head()`.

# In[133]:


category_counts.head()


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[134]:


category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()


# Examine `category_pivot`.

# In[135]:


category_pivot.head()


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[136]:


category_pivot.columns = ['category','not_protected','protected']
category_pivot


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[137]:


category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)


# Examine `category_pivot`.

# In[138]:


category_pivot


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?  - The data is categorical.
# - How many pieces of data are you comparing? - The sample size is 5824.

# In[139]:


#1 Figure Size = width 10, length 4
plt.figure(figsize=(10,4))
#2 Axes obect = ax - used for positioning labeling of x an y ticks
ax = plt.subplot()
#3 Create a bar chart - heights=percent protected of category_pivot
plt.bar(range(len(category_pivot.category)),category_pivot.percent_protected * 100)
#4,#5 Create x tick for each bar
pstat_labels = category_pivot.category
plt.xticks(range(len(category_pivot)),pstat_labels)
#6 label y axis
plt.ylabel('Percent Protected')
#7 Title graph
plt.title('Percent Protected by Species', fontsize = 25)
#8 Plot the graph
plt.show()


# #### Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[140]:


contingency = [[30,146],[75,413]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[141]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[142]:


_,pval,_,_=chi2_contingency(contingency)
print("pval = " + str(pval))
# Null Hypothesis is that there is no difference between the endangerment of mammals and birds.
# statistically significant is P < 0.05  (You would reject the NULL (H0) Hypothesis and say there is a difference)
# statistically highly significant is P < 0.001 (less than one in a thousand chance of being wrong).


# It looks like this difference isn't significant!   - P of 0.68 > 0.05
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[143]:


contingency = [[30,146],[5,73]]
_,pval,_,_=chi2_contingency(contingency)
print("pval = " + str(pval))


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!
# This means that some species are more likely than others to be endangered.

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[100]:


observations = pd.read_csv('observations.csv')
observations.head()


# In[101]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[102]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[103]:


species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
species.head()


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[104]:


species[species.is_sheep]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[105]:


sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
sheep_species.head()


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[106]:


sheep_observations = observations.merge(sheep_species)
sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[107]:


total_sheep = sheep_observations.observations.sum()
print(total_sheep)
obs_by_park = sheep_observations.groupby(['park_name']).observations.sum().reset_index()
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[144]:


#1 Figure Size = width 16, length 4
plt.figure(figsize=(16,4))
#2 Axes obect = ax - used for positioning labeling of x an y ticks
ax = plt.subplot()
#3 Create a bar chart - heights= observations of obs_by_park
plt.bar(range(len(obs_by_park.observations)),obs_by_park.observations)
#4,#5 Create x tick for each bar
obs_per_week_labels = obs_by_park.park_name
plt.xticks(range(len(obs_by_park)),obs_per_week_labels)
#6 label y axis
plt.ylabel('Number of Observations')
#7 Title graph
plt.title('Observations of Sheep per Week', fontsize = 25)
#8 Plot the graph
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage points.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use <a href="https://s3.amazonaws.com/codecademy-content/courses/learn-hypothesis-testing/a_b_sample_size/index.html">Codecademy's sample size calculator</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[109]:


#Baseline Conversion Rate:  15%
#Statistical Significance: 90%
#Minimum Detect. Effect:  100*.05 /.15 
mindeteffect = 100 * .05 /.15
mindeteffect


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[145]:


# Using a 33% MDE, the Code Academy Calculator gives a sample size of 890.  The Optimizley calculator gives a sample size of 520.  
# I would need to do more research, but could this be due to a difference in a two tailed versus a one tailed calculation?
# I will adopt the ore risky approach in this case to get a quicker estimate for our program. 
# Sample size = 520
#How Many Weeks?
Bryce_Sample_Size = 520 / 250 
print("Bryce_Sample_Size = " + str(Bryce_Sample_Size) + " weeks")
Yellowstone_Sample_Size = 520 / 507 
print("Yellowstone_Sample_Size = " + str(Yellowstone_Sample_Size) + " weeks")


# In[146]:


# We would need to collect samples for about 2 weeks at Bryce and about 1 week at Yellowstone.  

