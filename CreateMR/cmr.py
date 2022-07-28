#!/usr/bin/env python
#coding=utf-8

import sys
import os
import git


CHROME_PATH=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
CODE_DIR=r'D:\NetEco\01.code'
REPO_URL= 'https://codehub-y.huawei.com/y00801659'



def main():
    pwd = os.getcwd()
    # pwd = r'D:\NetEco\01.code\NetEcoBasicService\base'
    
    field = pwd.split('\\')
   
    basicDir = '\\'.join(field[0:4])
    # print('执行目录是:' + basicDir)
    
    projectName=field[3]
    # print('工程是:' + projectName)
    
    repo = git.Repo(basicDir)
    sourceBranch = str(repo.active_branch)
    targetBranch = str(repo.active_branch)
    # print('分支是:' + sourceBranch)

    cmd = '"' + CHROME_PATH + '" ' + REPO_URL + '/' + projectName + '/' + 'newmergeform?source_branch=' + sourceBranch # + '&target_branch=' + targetBranch
    # print(cmd)
    os.system(r"" + cmd + "")

if __name__ == '__main__': 
    main()

