import requests
import json
import pandas as pd
import re

API_key = "8f0eebd9f2b39c4d70818a8f6f6e6050"

df = pd.DataFrame(columns=['id', 'original_title', 'release_date', 'vote_average', 'vote_count', 'popularity', 'overview'])

for year in range(1980,2000):
    print(str(year))
    
    for page in range(1,50):
        responses = []
        url = "https://api.themoviedb.org/3/discover/movie?api_key="+ API_key +"&primary_release_year="+ str(year) +"&sort_by=revenue.desc&page="+str(page)
        response = requests.request("GET", url)
        data = json.loads(response.text)
        formattedData = json.dumps(data, indent=4)
        #print(formattedData)
        dataDict = json.loads(formattedData)
        #data we want is in .json {results}
        responses.append(dataDict["results"])

    #create empty dataframe
        #loop true movies and store attributes to dataframe
        for x in range(len(responses)):
            for movie in responses[x]:
                row_df = pd.DataFrame({'id':[movie['id']], 'original_title':[movie['original_title']], 'release_date':[movie['release_date']], 'vote_average':[movie['vote_average']], 'vote_count':[movie['vote_count']], 'popularity':[movie['popularity']], 'overview':[movie['overview']]})
                df = pd.concat([df, row_df], ignore_index=True)

df.to_csv('~/Documents/intro_to_DS/week3/example_data8.csv', encoding='utf-8')

stripped_df = (df[(df['vote_count'] > 0) & (df['overview'].notna()) & (df['overview'] != "")])
stripped_df.drop_duplicates(subset=['id'])
stripped_df.to_csv('~/Documents/intro_to_DS/week3/example_data9.csv', encoding='utf-8')

#call the API with the movie id's to get budget and revenue
#create new ds to store the genres, budgets and revenue, id is as a key to help merge the dataframes together later

#df = pd.read_csv('~/Documents/intro_to_DS/week3/example_data5.csv', lineterminator='\n')
 
new_df = pd.DataFrame(columns=['id', 'runtime', 'genres', 'budget', 'revenue'])

for index, row in stripped_df.iterrows():
    movie_id = row['id']
    url_string = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"?api_key="+API_key

    response2 = requests.request("GET", url_string)
    data2 = json.loads(response2.text)
    formattedData2 = json.dumps(data2, indent=4)
    #print(formattedData2)
    dataDict2 = json.loads(formattedData2)
    genre_string = ""
    for genre in dataDict2['genres']:
        string = str(genre).split()[-1]
        single_genre = re.sub(r'[^\w\s]', '', string)
        genre_string += single_genre+","
    
    genres = genre_string.rstrip(",")
    print(str(dataDict2['original_title']))
    row_df = pd.DataFrame({'id':dataDict2['id'], 'runtime':dataDict2['runtime'], 'genres':genres, 'budget':[dataDict2['budget']], 'revenue':[dataDict2['revenue']]})
    new_df = pd.concat([new_df, row_df], ignore_index=True)
   

result = pd.merge(stripped_df, new_df, on=["id"])
cols = result.columns.tolist()
cols = cols[:3] + cols[-4:] +cols[3:-4]
result_df = result[cols]

result_df.to_csv('~/Documents/intro_to_DS/week3/example_data10.csv', encoding='utf-8')

final_df = result_df[(result_df['budget'] != 0) & (result_df['revenue'] != 0) & (result_df['runtime'] > 60)]

final_df.to_csv('~/Documents/intro_to_DS/week3/example_data11.csv', encoding='utf-8')
