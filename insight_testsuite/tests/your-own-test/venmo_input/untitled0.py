#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 20:42:00 2017

@author: xlw
"""
with open('venmo-trans.txt','w') as out:
    with open('venmo-trans-raw.txt','r') as f:
        for line in f:
            text = line.split()
            print(text)
            newline = '{"' + text[6] + '": "' + text[7] + '", "' + text[3] + '": "' + text[5][:-1] + '", "' + text[0] + '": "' + text[2][:-1] + '"}'
            print(newline)
            out.write(newline + '\n')