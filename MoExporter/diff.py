#!/usr/bin/env python

import argparse
import json
import os
import sys
import csv

def load_record(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def main():

    oldFilename = sys.argv[1]
    newFilename = sys.argv[2]

    map2= {}
    for item in load_record(newFilename):
        dnId = item["dnId"]
        status = item["status"]
        map2[dnId] = status

    map1= {}
    for item in load_record(oldFilename):
        dnId = item["dnId"]
        status = item["status"]
        map1[dnId] = status

        if dnId not in map2.keys():
            print(f"deleted: {dnId}")
            continue
        previoudStatus = map1.get(dnId)
        newStatus = map2.get(dnId)
        if newStatus == previoudStatus:
            continue
        print(f'{dnId}, {previoudStatus}, {newStatus}')
        


if __name__ == '__main__':
    main()
