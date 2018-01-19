import json
import pandas as pd

rawjson = json.load(open('/Users/admin/gitprojects/mediabias/wordfreqs/final/output.json'))

df = pd.DataFrame()
for item in rawjson[:-1]:

    publication_date =  item['publication_date']
    doctype = item['doctype']

    crim_distance=[]
    crim_length = []
    crim_pair = []
    crim_position_w1 = []
    crim_position_w2 = []
    crim_type = []
    crim_publication_date = []
    crim_doctype = []
    low_distance=[]
    low_length = []
    low_pair = []
    low_position_w1 = []
    low_position_w2 = []
    low_type = []
    low_publication_date = []
    low_doctype = []
    if 'distance_criminal' in item:
        for d in item['distance_criminal']:
            crim_distance.append(d['distance'])
            crim_length.append(d['length'])
            crim_pair.append(d['pair'])
            crim_position_w1.append(d['position_w1'])
            crim_position_w2.append(d['position_w2'])
            crim_type.append('criminal')
            crim_publication_date.append(publication_date)
            crim_doctype.append(doctype)
        extrarows = pd.DataFrame.from_records(zip(crim_doctype,crim_publication_date, crim_type,crim_distance,crim_length,crim_pair,crim_position_w1,crim_position_w2))
        df = pd.concat([df,extrarows])
    if 'distance_low' in item:
        for d in item['distance_low']:
            low_distance.append(d['distance'])
            low_length.append(d['length'])
            low_pair.append(d['pair'])
            low_position_w1.append(d['position_w1'])
            low_position_w2.append(d['position_w2'])
            low_type.append('low')
            low_publication_date.append(publication_date)
            low_doctype.append(doctype)
        extrarows = pd.DataFrame.from_records(zip(low_doctype, low_publication_date, low_type,low_distance,low_length,low_pair,low_position_w1,low_position_w2))
        df = pd.concat([df,extrarows])

df.rename_axis({0:'doctype',1:'publication_date',2:'type',3:'distance', 4:'length_article',5:'word_pairs',6: 'position_w1', 7: 'position_w2'},axis=1, inplace=True)
df['id_binnen_artikel'] = df.index

df['word1'] = df.word_pairs.map(lambda x: x[0])
df['word2'] = df.word_pairs.map(lambda x: x[1])

df.to_csv('/Users/admin/gitprojects/mediabias/r_analyses/mediabias/wordfreqs/output_wordfreqs_nrc.csv')
