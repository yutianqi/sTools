#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name:     run.py
# Desc      The notepad++ can envolke this python script to run the code files by using a shortcut. 
#           The command can be like below: 
#           cmd /k cd /d "$(CURRENT_DIRECTORY)" & python "D:\Code\Github\sTools\Notepad++RunCode\run.py" "$(FULL_CURRENT_PATH)" & ECHO. & PAUSE & EXIT
# Author:   yutianqi 00290641    <yutianqi@huawei.com>
# Version:  2017/10/30 01:07:12  A sad and lost night.


import sys
import os

if len(sys.argv) == 1:
    print('No input filename.')
    exit(-1)

fileName = sys.argv[1]
extension = fileName.split('.')[-1]

cmdDict = {
            'py':'python',
            'go':'go run',
            'bat':'',
            'sh':'',
          }
          
#print '----> Begin to run the code: %s <----'  % fileName
print('---->  %s  <----'  % fileName)
        
if extension in cmdDict:
    os.system(cmdDict[extension] + ' "' + fileName + '"')

elif extension == 'java':  
    os.system('javac -encoding UTF-8 %s& java %s' % (fileName, '.'.join(fileName.split('\\')[-1].split('.')[:-1])))
else:
    print("Does not support the extension [%s]." % extension)


