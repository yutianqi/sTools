#!/usr/bin/env python
# coding=utf-8

import sys
import os
import subprocess
import logging
import git
import shutil
from time import sleep

def init_logger(logger):
    logger.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler("D:\\yutianqi\\Code\\Github\\sTools\\DailyPush\\log.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
    logger.addHandler(fileHandler)

    
def backup_files():
    shutil.copyfile("C:\\Users\\y00801659\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks", "D:\\yutianqi\\Notes\\Bookmarks")
    # shutil.copyfile("C:\\Users\\y00290641\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Bookmarks", "D:\\Notes\\Bookmarks_Duke")
    cmd = "D:\\Program Files\\Git\\usr\\bin\\dos2unix.exe D:\\yutianqi\\Notes\\Bookmarks"
    p = subprocess.Popen((cmd),stdout=subprocess.PIPE).stdout
    p.readlines()
    # subprocess.Popen((cmd))
    
  
def commit_files(repo, commitMessage):
    git_cmd = repo.git
    remote = repo.remote()	
    
    # 记录变更点
    for line in git_cmd.diff().splitlines():
        if line.startswith('-') or line.startswith('+'):
            logger.debug(line)
        
    git_cmd.add("./*")
    git_cmd.commit("-m", commitMessage)
    remote.push()
      
    
def main():
    sleep(2)
    if (len(sys.argv) > 1):
        commitMessage = sys.argv[1];
    else:
        commitMessage = "Daily commit from cloud desktop"

    backup_files()
    # return 
    repo = git.Repo("D:\\yutianqi\\Notes\\") 	
    if repo.is_dirty():
        commit_files(repo, commitMessage)
        logger.debug("Commited successfully.")
    else:
        logger.debug("Clean. No need to commit.")
    

if "__main__" == __name__:
    logger = logging.getLogger(__name__)
    init_logger(logger)
    main()
        
