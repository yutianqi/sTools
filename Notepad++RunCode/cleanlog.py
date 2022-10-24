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
    cleanFileName = fileName + ".clean"
    with open(cleanFileName, "w+", encoding="utf-8") as cleanFile:
        with open(fileName, "r", encoding="utf-8") as originFile:
            for inputStr in originFile.readlines():
                inputStr = re.sub("ne_cmd_.*.zip:\d{4}\-", "", str(inputStr))
                inputStr = re.sub(
                    "\[nioEventLoopGroup-\d+-\d+]\[ImodbusSubChannel.java \d+] ", "", str(inputStr))
                inputStr = re.sub(
                    "ImodbusSubChannel{channel=\[id: \w+, L:/.* - R:/.*], ", "", str(inputStr))
                inputStr = re.sub("isSsl=", "ssl=", str(inputStr))
                inputStr = re.sub(
                    "esn='.*', mainDevId=\d+}, packet=ImodbusPacket ", "pkg", str(inputStr))
                inputStr = re.sub("FuncCode", "FC", str(inputStr))
                inputStr = re.sub("subCode", "SC", str(inputStr))
                inputStr = re.sub("SerialNum", "SN", str(inputStr))
                inputStr = re.sub("sendCmd", "send", str(inputStr))
                inputStr = re.sub("recvCmd", "recv", str(inputStr))
                inputStr = re.sub("reqType='null', ", "", str(inputStr))

                cleanFile.write(inputStr)
    call(('D:\\Program Files\\Notepad++\\notepad++.exe', cleanFileName))

if __name__ == "__main__":
    main()
