#!/usr/bin/env python

import json
import os
import sys
import requests
import time

HEADERS = {'content-type': 'application/json'}
QUERY_API = '/rest/neteco/modelmgr/v1/mo/by-advanced-conditions'
BATCH_QUERY_LIMIT = 4000
NAME_SPACE = ""
DN_FILE_NAME = "_dn.json"
MO_FILE_NAME = "_mo.json"


def send_request(url, dnIdList):
    response = requests.post(url, data=json.dumps(
        dnIdList), headers=HEADERS, verify=False)
    if str(response.status_code) != '200':
        raise SystemError(f'Invalid status code. response: {response.text}')
    response = json.loads(response.text)
    return response


def getStatusMap(mo_info_list):
    beginIndex = 0
    statusMap = {}
    ip = os.popen(
        f'kubectl get svc -n {NAME_SPACE} | grep dpmodelproxyservice | sed -r "s/ +/,/g" | cut -d "," -f3').readlines()[0].strip()
    url = f"http://{ip}:8080/rest/neteco/modelmgr/v1/mo/instances/dn-ids"
    while beginIndex < len(mo_info_list) - 1:
        endIndex = beginIndex + BATCH_QUERY_LIMIT
        if endIndex >= len(mo_info_list):
            endIndex = len(mo_info_list)-1

        print(f'  > Query {beginIndex} - {endIndex}')
        dnIdList = [str(item["dnId"])
                    for item in mo_info_list[beginIndex: endIndex]]

        response = send_request(url, dnIdList)
        for item in response:
            statusMap[item["dnId"]] = item["status"]
        beginIndex = endIndex
    return statusMap


def save_result(file_name, result_list):
    f = open(file_name, 'w')
    f.write(json.dumps(result_list, indent=4))
    f.close()


def load_record(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def main():
    if (len(sys.argv) > 1):
        global NAME_SPACE
        global DN_FILE_NAME
        global MO_FILE_NAME
        NAME_SPACE = sys.argv[1]
        DN_FILE_NAME = NAME_SPACE + "_dn.json"
        MO_FILE_NAME = NAME_SPACE + "_mo.json." + \
            time.strftime("%Y%m%d_%H%M%S", time.localtime())
    else:
        return
    input(NAME_SPACE)

    mo_info_list = load_record(DN_FILE_NAME)
    print(f"> Finished to load mo info, size={len(mo_info_list)}")

    statusMap = getStatusMap(mo_info_list)
    print(f"> Finished to get status map, size={len(statusMap)}")

    keys = statusMap.keys()
    for item in mo_info_list:
        dnId = item["dnId"]
        if dnId in keys:
            item["status"] = statusMap[dnId]
        else:
            print(f"> Cannot find the status of [{dnId}]")

    print(f"> Finished to update, save result to {MO_FILE_NAME}")
    save_result(MO_FILE_NAME, mo_info_list)


if __name__ == '__main__':
    main()
