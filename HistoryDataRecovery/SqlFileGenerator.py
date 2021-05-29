#!/usr/bin/env python
#coding=utf8


import requests
import json
import time

inFileName = 'data.csv'
outFileName = 'data.sql'

FIELD_NUM = 10

TBL_NAME = 'tbl_pm_data'

def updateFile():
    lines = []
    with open(inFileName, 'r') as inFile:
        for index,line in enumerate(inFile.readlines()):
            line = line.strip()
            if line.startswith('#'):
                continue
            fields = line.split(',')
            if len(fields) != FIELD_NUM:
                print('line {0} is invalid. Please check.'.format(index + 1))
                return
            # print(index, line.strip())
            if fields[-2] != fields[-1]:
                print('{},{}'.format(fields[-2], fields[-1]))
                lines.append(fields)
                
    print(len(lines))
    return lines

    
def save(inLines):
    
    with open(outFileName, 'w+', encoding='utf-8') as f:
        f.writelines('# INFLUXDB EXPORT: 1677-09-21T08:12:43+08:00 - 2262-04-12T07:47:16+08:00\n')
        f.writelines('# DDL\n')
        f.writelines('CREATE DATABASE pmdb_2 WITH NAME rp_scale_1\n')

        f.writelines('# DML\n')
        f.writelines('# CONTEXT-DATABASE:pmdb_2\n')
        f.writelines('# CONTEXT-RETENTION-POLICY:rp_scale_1\n')
        f.writelines('# writing wal data\n')

        for line in inLines:
            #dnId,retentionPolicyName,counterId,localDateTime,startTime,timeZoneOffset,dstOffset,counterValue,newCounterValue
            dnId = line[0]
            counterId = line[2]
            counterValue = line[8]
            startTime = line[4]
            
            f.writelines('{},dn_id={} counter_{}={} {}000000000\n'.format(TBL_NAME, dnId, counterId, counterValue, startTime))
            


def main():
    lines = updateFile()
    
    save(lines)
    
    

if __name__ == '__main__':
    main()
    
