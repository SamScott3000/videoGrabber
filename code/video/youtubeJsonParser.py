import pandas as pd
import json

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 5000)

pd.set_option("display.max_rows", None, "display.max_columns", None)

fileName = 'youtubeSearch'

f = open(f'{fileName}.json')

with open(f'{fileName}.json') as data_file:
    data = json.load(data_file)
norm = pd.json_normalize(data, record_path=['items'])

df = pd.DataFrame(norm)

newDf= df[['snippet.title']].copy()

youtubeLink = 'https://www.youtube.com/watch?v='

newDf['videoLink'] = youtubeLink + df[['id.videoId']]

newDf['snippet.publishTime'] = df[['snippet.publishTime']]
newDf['id.videoId'] = df[['id.videoId']]
