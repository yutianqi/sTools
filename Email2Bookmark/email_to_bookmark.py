# encoding=utf8
import win32com.client
import win32com
import os
import sys


# 目标发件人列表
SENDER_SET = {"tianqi.yu@icloud.com", "352168337@qq.com"}

# FOLDER_LIST = [ "tianqi.yu", "收件箱"]
SCAN_FOLDER_SET = {"收件箱"}

REPLACE_MAP = {
    "发自我的iPhone": "",
    "发自我的 iPhone": ""
}


def filterMessages(folder):
    messages = []
    total = len(folder.Items)
    if total == 0:
        return messages
    print(f"Total: {total}")
    # lines = []
    for message in folder.Items:
        try:
            sender = message.SenderEmailAddress
            print(f"> {message.Subject.strip()}")
            if sender not in SENDER_SET:
                continue
            messages.append(message)
            # TODO
            # print(dir(message))
            # return messages
        except Exception as e:
            print(e)
            pass
        # try:
        #     message.Save()
        #     message.Close(0)
        # except:
        #     pass
        # i += 1
    # return lines
    messages.sort(key=lambda item: item.CreationTime)
    return messages


def save(messages):
    if not messages:
        return
    with open("bm.txt", "a+", encoding='utf-8') as fobj:
        i = 1
        for message in messages:
            # ids = "\r\n# " + str(i) + "\r\n"

            fobj.write(message.CreationTime.strftime("%Y-%m-%d %H:%M:%S"))
            fobj.write("\n")
            fobj.write(message.Subject.strip())
            fobj.write(": \n")
            content = message.Body
            for (key, value) in REPLACE_MAP.items():
                content = content.replace(key, value)
            fobj.write(content.strip())
            fobj.write("\n\n")
            i += 1


def move(messages, backupFolder):
    if not messages:
        return
    for message in messages:
        message.Move(backupFolder)
    print("Moved")


def getFoldersByName(inbox, name):
    folders = inbox.Folders
    for folder in folders:
        if name != folder.Name:
            continue
        return folder
    return None


def main():
    outlook = win32com.client.Dispatch(
        "Outlook.Application").GetNamespace("MAPI")
    accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts
    for account in accounts:
        print(account.DisplayName)
        inbox = outlook.Folders(account.DeliveryStore.DisplayName)
        folders = inbox.Folders
        backupFolder = getFoldersByName(inbox, "tianqi.yu")
        if not backupFolder:
            print(f"Cannot find backup folder")
            continue
        for folder in folders:
            if folder.Name not in SCAN_FOLDER_SET:
                continue
            print("Folder Name: " + folder.Name)
            messages = filterMessages(folder)
            save(messages)
            move(messages, backupFolder)
    print("Finished Succesfully")


if __name__ == '__main__':
    main()

