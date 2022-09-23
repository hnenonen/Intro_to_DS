import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale
import math
import seaborn as sns

def load_data():
    data = pd.read_csv('Data/data_1980to2000.csv')
    
    #DROP UNNECESSARY COLUMNS    
    data.drop(columns=['id', 'overview', 'Unnamed: 0'], inplace=True)
    data.set_index('original_title', inplace=True)
    data['release_date'] = pd.to_datetime(data['release_date'])

    #CHANGE DATE TO DATETIME, SPLIT DATE (for now)
    data['release_month'] = data['release_date'].dt.month
    
    # day/year not needed (for now)
    data['release_year'] = data['release_date'].dt.year
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

def year_stuff(df):
    curr_year = datetime.date.today().year
    max = math.log(curr_year-1980)

    df['release_year_scaled'] = df['release_year'].apply(lambda x: 10*math.log(x-1980)/max if x-1980!=0 else 0)
    
    #plt.scatter(df['release_year'], df['release_year_scaled'])
    #plt.show()

def normal_dist(x , mean , sd):
        prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
        return prob_density


from scipy.stats import norm
def runtime(df):
    x = scale(df['runtime'])
    
    #Calculate mean and Standard deviation.
    mean = np.mean(df['runtime'])
    sd = np.std(df['runtime'])
    Z = (abs((df['runtime']-mean))/sd)
    print(max(Z), min(Z))
    df['runtime_multiplier'] = Z.apply(lambda x: 10-x**2)
    print(df[['runtime','runtime_multiplier']].describe())


def main():

    data = load_data()
    #sns.histplot(data['runtime'])
    #plt.show()
    runtime(data)

    #year_stuff(data)
    #print(data['popularity']*10e-2)
    #print(data['revenue'].apply(lambda x: math.log(x)))
    #data = add_goodness_factor(data)
    #print(data['release_year'])
    #seaborn_plots(data, 'rating>7')


if __name__ == "__main__":
    main()
