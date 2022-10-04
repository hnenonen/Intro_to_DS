import pandas as pd

def evaluate(text):
    worth_watch = "BAD"
    estimated_runtime = 180 
    estimated_gross = 9999
    estimated_voteaverage = 5.0

    # text for analysis 
    if len(text) > 100:
        worth_watch = "GOOD"
        estimated_runtime = 120
        estimated_gross = 239999
        estimated_voteaverage = 9.0

    return(worth_watch, estimated_runtime, estimated_gross, estimated_voteaverage)

def recommendation():
    df = pd.read_csv('Data/data_processed_final.csv')
    recommendations = (df[ df["goodness_factor"] > 7.48].sample(3))
    list = []
    for index, recommendation in recommendations.iterrows():
        id = recommendation["id"] 
        title = recommendation["original_title"] 
        goodness = round(recommendation["goodness_factor"], 2)
        movie = [id, title, goodness]
        list.append(movie)
    return(list)

print(recommendation())