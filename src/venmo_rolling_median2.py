#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 22:33:25 2017

@author: xlw
"""

import pandas as pd
import numpy as np
    
def extract_actor_target_time(transaction):
    from datetime import datetime
    splits = transaction.split()
    time_raw = splits[1][1:][:-2]
    time = datetime.strptime(time_raw,'%Y-%m-%dT%H:%M:%SZ')
    actor = splits[5][1:][:-2]
    target = splits[3][1:][:-2]
    return actor, target, time
    
def func(x,latest):
    return get_interval(latest, x) < 60
    
def update(df):
    check_duplicate(df)
    latest = max(df.time)
    df['criterion'] = df['time'].apply(lambda x: get_interval(latest,x) < 60)    
    return df[df['criterion']==True]

def check_duplicate(df):
    latest_actor = df.iloc[-1]['actor']
    latest_target = df.iloc[-1]['target']
#    if there is a record with the same actor and target:
#        keep the latests one
    return df
    
def is_within_window(df,time):
    if len(df) == 0:
        return True
    else:
        return get_interval(time,max(df.time)) < 60
        
def is_in_order(df,time):
    if len(df) == 0:
        return True
    else:
        return get_interval(time,df.iloc[-1].time) > 0
                        
def get_interval(time1,time2):
    #returns time difference in seconds
    diff = time1 - time2
    return diff.days*86400 + diff.seconds
def get_graph(df):
    graph = {}
    for actor in df.actor.values:
        if actor not in graph:
            graph[actor] = 1
        else:
            graph[actor] += 1
    for target in df.target.values:
        if target not in graph:
            graph[target] = 1
        else:
            graph[target] += 1
    return graph
def get_median(graph):
    counts = sorted(graph.values())
    return '%.2f' % np.median(counts)
    
with open('./venmo_input/venmo-trans.txt','r') as infile:
    medians = []
    df = pd.DataFrame(columns=['actor','target','time'])
    for line in infile:
        actor, target, time = extract_actor_target_time(line)
        if not is_in_order(df,time) and not is_within_window(df,time):
            next
        else:        
            df=df.append({'actor':actor,'target':target,'time':time},ignore_index=True)
            df = update(df)
            graph = get_graph(df)
#            print(graph)
            medians.append(get_median(graph))
            print(medians[-1])
with open('./venmo_output/output.txt','w') as outfile:
    outfile.write('\n'.join(str(i) for i in medians))
    