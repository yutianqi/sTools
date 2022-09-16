#!/usr/bin/env python
# coding=utf-8

import sys
import os
import logging
import git
import shutil
from time import sleep

def init_logger(logger):
    logger.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler("D:\\yutianqi\\Code\\sTools\\DailyPush\\log.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'))
    logger.addHandler(fileHandler)

    
def backup_files():
    shutil.copyfile("C:\\Users\\y00290641\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks", "D:\\yutianqi\\Notes\\Bookmarks")
    # shutil.copyfile("C:\\Users\\y00290641\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Bookmarks", "D:\\Notes\\Bookmarks_Duke")
    print("dos2unix.exe D:\\yutianqi\\Notes\\Bookmarks")
    os.system("dos2unix.exe D:\\yutianqi\\Notes\\Bookmarks")
    
  
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
        
