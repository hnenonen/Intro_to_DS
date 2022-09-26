from audioop import minmax
from itertools import count
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import scale
import math
import seaborn as sns

def load_data():
    data = pd.read_csv('Data/data_1980to2000.csv')
    
    #DROP UNNECESSARY COLUMNS    
    data.drop(columns=['id', 'overview', 'Unnamed: 0'], inplace=True)
    data.set_index('original_title', inplace=True)
    data['release_date'] = pd.to_datetime(data['release_date'])

    #CHANGE DATE TO DATETIME, SPLIT DATE
    data['release_month'] = data['release_date'].dt.month
    data['release_year'] = data['release_date'].dt.year
    
    # day not needed (for now)
    #data['release_day'] = data['release_date'].dt.day
    
    #Drop date column
    data.drop(columns=['release_date'], inplace=True)
    
    return data    

def add_goodness_factor(data):
    data['rating>7'] = data['vote_average'].apply(lambda x: 1 if x>7 else 0)
    vote_multiplier = 1-10/data['vote_count']
    data['log_revenue'] = data['revenue'].apply(lambda x: math.log(x))
    data['log_popularity'] = data['popularity'].apply(lambda x: math.log(x))

    data['goodness'] = (data['vote_average']*vote_multiplier + data['log_revenue'])#+data['log_popularity']
    
    #??
    data.drop(columns=['revenue', 'popularity'], inplace=True)
    
    reshaped_goodness = data['goodness'].array.reshape(-1, 1)
    asd = scale(reshaped_goodness)
    data['goodness'] = asd
    return data

def seaborn_plots(data, split=None):
    #test_batch = data[['vote_count', 'release_month']]
    #print(test_batch.head())
    
    sns.pairplot(data, hue=split)
    plt.show(block=True)


import datetime

def add_freshness(df):
    curr_year = datetime.date.today().year
    max = math.log(curr_year-1980)

    df['freshness'] = df['release_year'].apply(lambda x: 10*math.log(x-1980)/max if x-1980!=0 else 0)


#probs not needed
def normal_dist(x , mean , sd):
        prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
        return prob_density

def add_runtime_mult(df):
    #Calculate mean and Standard deviation.
    mean = np.mean(df['runtime'])
    sd = np.std(df['runtime'])
    
    Z = (abs((df['runtime']-mean))/sd)
    df['runtime_multiplier'] = Z.apply(lambda x: 10-x**2)
    df['runtime_multiplier'][df['runtime_multiplier']<0].apply(lambda x: 0)

def add_vote_x_avg(df):
    count_x_avg = df['vote_count']*df['vote_average']    
    min_val, max_val = min(count_x_avg), max(count_x_avg)

    count_x_avg = count_x_avg.apply(lambda x: 10*math.log(x-min_val)/math.log(max_val-min_val) if x-min_val>0 else 0)
    
    df['count_x_avg'] = count_x_avg
    
    #df.plot(y='count_x_avg')
    #plt.show()
    #print(count_x_avg.describe())

def add_gross(df):
    gross = df['revenue']-df['budget']
    min_val, max_val = min(gross), max(gross)

    gross = gross.apply(lambda x: 10*math.sqrt(x-min_val)/math.sqrt(max_val-min_val) if x-min_val>0 else 0)
    
    df['gross'] = gross

    df.plot(y='gross')
    plt.show()
    #print(df[['revenue', 'gross']])
    #print(df[['revenue', 'budget']][df['gross']<1]) 


def main():

    data = load_data()
    #add_gross(data)
    #add_vote_x_avg(data)
    #add_freshness(data)
    #add_runtime_mult(data)


if __name__ == "__main__":
    main()
