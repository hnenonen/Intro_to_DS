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
