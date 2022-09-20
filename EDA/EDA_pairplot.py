import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path

def load_data():
    data = pd.read_csv('Data/example_data.csv')
    
    #DROP UNNECESSARY COLUMNS    
    data.drop(columns=['id', 'overview', 'Unnamed: 0'], inplace=True)
    data.set_index('original_title', inplace=True)
    data['release_date'] = pd.to_datetime(data['release_date'])

    #CHANGE DATE TO DATETIME, SPLIT DATE (for now)
    data['release_month'] = data['release_date'].dt.month
    
    # day/year not needed (for now)
    #data['release_year'] = data['release_date'].dt.year
    #data['release_day'] = data['release_date'].dt.day
    
    #Drop date column
    data.drop(columns=['release_date'], inplace=True)
    
    return data    

def add_goodness_factor(data):
    data['rating>7'] = data['vote_average'].apply(lambda x: 1 if x>7 else 0)
    return data

def seaborn_plots(data, split=None):
    #test_batch = data[['vote_count', 'release_month']]
    #print(test_batch.head())
    
    sns.pairplot(data, hue=split)
    plt.show(block=True)

def main():
    data = load_data()
    data = add_goodness_factor(data)
    seaborn_plots(data, 'rating>7')


if __name__ == "__main__":
    main()
