
#!/usr/bin/python
# encoding=utf8

# Name:     cleanlog.py
# Author:   yutianqi 00801659    <yutianqi@huawei.com>
# Version:  2022/10/24 17:57:59  Happy programmer's day

import sys
import re

from subprocess import call


def main():
    if len(sys.argv) == 1:
        print('No input filename.')
        exit(-1)
    fileName = sys.argv[1]
    reverseFileName = fileName + ".reverse"
    process(fileName, reverseFileName)

    call(('D:\\Program Files\\Notepad++\\notepad++.exe', reverseFileName))

def processBak(fileName, reverseFileName):
    lines = []
    with open(fileName, "r", encoding="utf8") as fobj:
        for line in fobj.readlines():
            # print(line)
            lines.append(line)
    with open(reverseFileName, "w", encoding="utf8") as fobj:        
        fobj.writelines(sorted(lines[::-1]))

def process(fileName, reverseFileName):
    linesMap = {}
    with open(fileName, "r", encoding="utf8") as fobj:
        for line in fobj.readlines():
            line = line.strip()
            if not line:
                continue
            print(line)
            # ^(202\d\-)?\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}(.\d{3})
            fileds = line.split(" ")
            print(fileds[0] + fileds[1] + fileds[2] + fileds[3])

            sortKey = fileds[0] + fileds[1]        
            if sortKey not in linesMap:
                linesMap[sortKey] = []
            linesMap[sortKey].append(line)

    with open(reverseFileName, "w+", encoding="utf8") as fobj: 
        for item in sorted(linesMap.keys()):
            print(item)
            # print(linesMap.get(item)[::-1])
            for line in linesMap.get(item)[::-1]:
                fobj.write(line + "\n")
        

if __name__ == "__main__":
    main()


    




