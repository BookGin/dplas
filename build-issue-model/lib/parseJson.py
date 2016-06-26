#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys

# usage: ./parseJson.py input output

def parse(string):
    data = json.loads(string)
    for obj in data:
        if obj["topic"] == int(sys.argv[2]):
            for i in obj["content"]:
                print(i, end=" ")
            print()

string = ""
with open(sys.argv[1], 'r', encoding='UTF-8') as f:
    inputdata = f.readlines()
    for i in inputdata:
        string += i
parse(string)
