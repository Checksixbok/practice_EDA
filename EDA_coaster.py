
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

plt.style.use('ggplot')
#pd.set_option('max_columns', 200)

#import data
df = pd.read_csv('coaster_db.csv')

##Data understanding
 #Dataframe shape
 #head and tail
 #dtypes
 #describe

df.shape
df.head(5)
df.columns
df.dtypes
df.describe()

## Step 2: Data Preperation
   #Dropping irrelevant columns and rows
   #Identifying duplicated columns
   #Renaming Columns
   #Feature Creation

 # Example of dropping columns
  
    # df.drop(['Opening date'], axis=1)
df = df[['coaster_name',
    # 'Length', 'Speed',
    'Location', 'Status',
    # 'Opening date',
    #   'Type',
    'Manufacturer',
#     'Height restriction', 'Model', 'Height',
#        'Inversions', 'Lift/launch system', 'Cost', 'Trains', 'Park section',
#        'Duration', 'Capacity', 'G-force', 'Designer', 'Max vertical angle',
#        'Drop', 'Soft opening date', 'Fast Lane available', 'Replaced',
#        'Track layout', 'Fastrack available', 'Soft opening date.1',
#        'Closing date',
#     'Opened', 
    # 'Replaced by', 'Website',
#        'Flash Pass Available', 'Must transfer from wheelchair', 'Theme',
#        'Single rider line available', 'Restraint Style',
#        'Flash Pass available', 'Acceleration', 'Restraints', 'Name',
       'year_introduced',
        'latitude', 'longitude',
    'Type_Main',
       'opening_date_clean',
    #'speed1', 'speed2', 'speed1_value', 'speed1_unit',
       'speed_mph', 
    #'height_value', 'height_unit',
    'height_ft',
       'Inversions_clean', 'Gforce_clean']].copy()

df.shape

df.dtypes

# It is date variable, so we need to change 'object' to 'datetime'

df['opening_date_clean'] = pd.to_datetime(df['opening_date_clean'])

# When we neet to change dtype:string to numeric.
pd.to_numeric(df['year_introduced'])

# Rename our columns
df = df.rename(columns={'coaster_name':'Coaster_Name',
                   'year_introduced':'Year_Introduced',
                   'opening_date_clean':'Opening_Date',
                   'speed_mph':'Speed_mph',
                   'height_ft':'Height_ft',
                   'Inversions_clean':'Inversions',
                   'Gforce_clean':'Gforce'})

df.head(5)

#check missing values

df.isna().sum()

#check duplicates

df.loc[df.duplicated()]

df.duplicated().sum()

# Check for duplicate coaster name

df.duplicated(subset=['Coaster_Name']).sum()

df.loc[df.duplicated(subset=['Coaster_Name'])].head(5)

# Checking an example duplicate
df.query('Coaster_Name == "Crystal Beach Cyclone"')

df.columns

# locate 'Not dupilcates'
df.loc[~df.duplicated(subset=['Coaster_Name','Location','Opening_Date'])]

df = df.loc[~df.duplicated(subset=['Coaster_Name','Location','Opening_Date'])] \
    .reset_index(drop=True).copy()

df.shape

###Step 3: Feature Understanding
 ##(Univariate analysis)

   #Plotting Feature Distributions
   #Histogram
   #KDE
   #Boxplot

#Count unique vaulues in certain column

df['Year_Introduced'].value_counts()

df['Year_Introduced'].value_counts().head(10)

#histogram
ax = df['Year_Introduced'].value_counts() \
    .head(10) \
    .plot(kind='bar', title='Top 10 Years Coasters Introduced')
ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')

#change bin 
ax = df['Speed_mph'].plot(kind='hist',
                          bins=20,
                          title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')

#density 
ax = df['Speed_mph'].plot(kind='kde', title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')

# count 
df['Type_Main'].value_counts()

###Step 4: Feature Relationships
  #Scatterplot
  #Heatmap Correlation
  #Pairplot
  #Groupby comparisons

#Scatterplot
#scatterplot built in pandas     
df.plot(kind='scatter',
        x='Speed_mph',
        y='Height_ft',
        title='Coaster Speed vs. Height')
plt.show()

#scatterplot in seaborn
ax = sns.scatterplot(x='Speed_mph',
                y='Height_ft',
                hue='Year_Introduced',
                data=df)
ax.set_title('Coaster Speed vs. Height')
plt.show()

#Pairplot
sns.pairplot(df,
             vars=['Year_Introduced','Speed_mph',
                   'Height_ft','Inversions','Gforce'],
            hue='Type_Main')
plt.show()

##Correlation

#correlation_matrix
df_corr = df[['Year_Introduced','Speed_mph',
    'Height_ft','Inversions','Gforce']].dropna().corr()
df_corr

#heatmap_correlation
sns.heatmap(df_corr, annot=True)

###Step 5: Ask a Question about the data
 ##Try to answer a question you have about the data using a plot or statistic.
   
   #What are the locations with the fastest roller coasters (minimum of 10)?

ax = df.query('Location != "Other"') \
    .groupby('Location')['Speed_mph'] \
    .agg(['mean','count']) \
    .query('count >= 10') \
    .sort_values('mean')['mean'] \
    .plot(kind='barh', figsize=(12, 5), title='Average Coast Speed by Location')

ax.set_xlabel('Average Coaster Speed')

plt.show()
