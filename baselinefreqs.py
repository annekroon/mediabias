#!/usr/bin/env python3

import inca
words = [w.strip() for w in open('ressources/words_target.txt').readlines() if len(w.strip())>0]




fromdate = '1991-01-01'
todate = '2017-12-31'
listofdoctypes = ['ad (print)','nrc (print)','volkskrant (print)','telegraaf (print)', 'trouw (print)']


analyzer = inca.analysis.timeline_analysis.timeline_generator()

for word in words:
    print('Now counting articles containing "{}"'.format(word))
    q = {"query": {
            "bool": {
                           "must": [{"query_string" : {"query" : word}}],
                        "filter": [ {'bool': {'should': [{ "match": { "doctype.keyword": d}} for d in listofdoctypes]}},
                                          { "range": { "publication_date": { "gte": fromdate, "lt":todate }}}]}
            }}

    doctypequery = "doctype:"+" OR doctype:".join(['"{}"'.format(d) for d in listofdoctypes])
    qs  = '{} AND ({})' .format(word,doctypequery)
    print(qs)
    
    df = analyzer.analyse(queries = qs, granularity='year',timefield='publication_date',from_time='1991-01-01')
    df.to_csv('output/baselinecount-{}.csv'.format(word))
