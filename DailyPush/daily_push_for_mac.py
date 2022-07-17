#!/usr/bin/env python3
# coding=utf-8

import sys
import logging
import git
import shutil
from time import sleep

def backup_files():
    shutil.copyfile("/Users/yutianqi/Library/Application Support/Google/Chrome/Default/Bookmarks", "/Users/yutianqi/Notes/Bookmarks")
    
def commit_files(repo, commitMessage):
    git_cmd = repo.git
    remote = repo.remote()	
    
    # 记录变更点
    # for line in git_cmd.diff().splitlines():
    #     if line.startswith('-') or line.startswith('+'):
    #         pass
        
    git_cmd.add("./*")
    git_cmd.commit("-m", commitMessage)
    remote.push()      
    
def main():
    # sleep(2)
    if (len(sys.argv) > 1):
        commitMessage = sys.argv[1];
    else:
        commitMessage = "Daily commit from cloud desktop"

    backup_files()
    repo = git.Repo("/Users/yutianqi/Notes/") 	
    if repo.is_dirty():
        commit_files(repo, commitMessage)
        print("Commited successfully.")
    else:
        print("Clean. No need to commit.")
    

if "__main__" == __name__:
    main()
        
