import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns

def load_data():
    data = pd.read_csv('Data/data_processed.csv')
    
    #DROP UNNECESSARY COLUMNS    
    data.drop(columns=['id', 'overview', 'Unnamed: 0'], inplace=True)
    data.set_index('original_title', inplace=True)

    #Drop date column
    data.drop(columns=['release_date', 'Unnamed: 0.1'], inplace=True)
    
    return data    

def add_goodness_factor(df):
    goodness_factor = 0.25*df['gross_factor'] + 0.25*df['pop_factor'] + 0.25*df['freshness_factor'] + 0.25*df['runtime_factor']
    df['goodness_factor'] = goodness_factor

def seaborn_plots(data, split=None):
    #test_batch = data[['vote_count', 'release_month']]
    #print(test_batch.head())
    
    sns.pairplot(data, hue=split)
    plt.show(block=True)


import datetime

def add_freshness_factor(df):
    curr_year = datetime.date.today().year
    max = math.log(curr_year-1980)

    df['freshness_factor'] = df['year'].apply(lambda x: 10*math.log(x-1980)/max if x-1980!=0 else 0)

def add_runtime_factor(df):
    #Calculate mean and Standard deviation.
    mean = np.mean(df['runtime'])
    sd = np.std(df['runtime'])
    Z = (abs((df['runtime']-mean))/sd)
    inverse_Z = (mean/sd)/Z

    min_val, max_val = min(inverse_Z), max(inverse_Z)
    runtime_factor = inverse_Z.apply(lambda x: 10*math.log(x-min_val)/math.log(max_val-min_val) if x-min_val>0 else 0)
    df['runtime_factor'] = runtime_factor
    df.loc[df['runtime_factor']<0, 'runtime_factor'] = 0

    #old method without inverse
    #df['runtime_factor'] = Z.apply(lambda x: 10-x**2)
    
def add_pop_factor(df):
    count_x_avg = df['vote_count']*df['vote_average']    
    min_val, max_val = min(count_x_avg), max(count_x_avg)

    count_x_avg = count_x_avg.apply(lambda x: 10*math.log(x-min_val)/math.log(max_val-min_val) if x-min_val>0 else 0)
    
    df['pop_factor'] = count_x_avg
    
    #df.plot(y='count_x_avg')
    #plt.show()
    #print(count_x_avg.describe())

#fixed_budget,fixed_revenue,fixed_gross
def add_gross_factor(df):
    gross = df['fixed_gross']
    min_val, max_val = min(gross), max(gross)

    gross = gross.apply(lambda x: 10*math.sqrt(x-min_val)/math.sqrt(max_val-min_val) if x-min_val>0 else 0)
    
    df['gross_factor'] = gross

    #df.plot(y='gross_factor')
    #plt.show()
    #print(df[['revenue', 'gross']])
    #print(df[['revenue', 'budget']][df['gross']<1]) 

def popularity_vs_goodness(df):
    # Tried to scale popularity down, bad result:
    #
    #min_val, max_val = min(data['popularity']), max(data['popularity'])
    #data['popularity_scaled'] = data['popularity'].apply(lambda x: 10*(x-min_val)/(max_val-min_val))
    
    tmpr_data = df[['goodness_factor', 'popularity']]
    
    #Correlation:
    #print(tmpr_data.corr())
    
    tmpr_data.sample(n=15).plot(grid=True)
    plt.show()
    print(tmpr_data.sort_values(by='goodness_factor'))
    print(tmpr_data.sort_values(by='popularity'))

import os
def save_results(df):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../Data/data_processed_final.csv')
    df.to_csv(filename, encoding='utf-8')

def main():

    data = load_data()

    add_gross_factor(data)
    add_pop_factor(data)
    add_freshness_factor(data)
    add_runtime_factor(data)
    add_goodness_factor(data)
    #print(data[['gross_factor', 'pop_factor', 'freshness_factor', 'runtime_factor']])
    
    save_results(data)

    
if __name__ == "__main__":
    main()
