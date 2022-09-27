import pandas as pd
from itertools import islice

df_2020 = pd.read_csv('~/Documents/intro_to_DS/week3/example_data11.csv', lineterminator='\n')
df_1980 = pd.read_csv('~/Documents/intro_to_DS/week3/example_data7.csv', lineterminator='\n')

df_total = pd.concat([df_2020, df_1980], ignore_index=True)
df_time = pd.DataFrame(columns=['year', 'month', 'day'])

years = []
months = []
days = []

for index, row in df_total.iterrows():
    year = (row['release_date'].split("-")[0])
    month = (row['release_date'].split("-")[1])
    day = (row['release_date'].split("-")[2]) 
    years.append(year)
    months.append(month)
    days.append(day)
df_time = pd.DataFrame({'year':years, 'month':months, 'day':days})
df_time['year'] = df_time['year'].astype(int) 
df_time['month'] = df_time['month'].astype(int) 
df_time['day'] = df_time['day'].astype(int) 

df_processed = pd.concat([df_total, df_time], axis=1)

df_inflation = pd.read_csv('inflation_data.csv')
print(list(df_inflation))

def inflation_calc(budget, revenue, year):    
    multiplier = 0
    for index, row in islice(df_inflation.iterrows(), 0, None):
        budget = budget * (1+multiplier)
        revenue = revenue * (1+multiplier)
        if row['    year'] >= year:
            #print(row['year'], sum)
            multiplier = (row['inflation rate'])
    return(budget, revenue, revenue-budget)

df_fixed_inflation = pd.DataFrame(columns=['id', 'fixed_budget', 'fixed_revenue', 'fixed_gross'])

for index, row in df_processed.iterrows():
    budget, revenue, gross = (inflation_calc(row['budget'], row['revenue'], row['year']))
    #print(budget, revenue, gross)
    fixed_row = pd.DataFrame({'id':row['id'], 'fixed_budget':[budget], 'fixed_revenue':[revenue], 'fixed_gross':[gross]})
    df_fixed_inflation = pd.concat([df_fixed_inflation, fixed_row], ignore_index=True)



result = pd.merge(df_processed, df_fixed_inflation, on=["id"])
#print(result)
result.to_csv('~/Intro_to_DS/Data/data_processed.csv', encoding='utf-8')
print("hep")