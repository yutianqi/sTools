#!/usr/bin/env python

import json
import os
import sys
import requests
import time

HEADERS = {'content-type': 'application/json'}
QUERY_API = '/rest/neteco/modelmgr/v1/mo/by-advanced-conditions'
BATCH_QUERY_LIMIT = 4000
MAX_QUERY_TIME_LIMIT = 1000
ESN_SIG_QUERY_LIMIT = 1000
NAME_SPACE = "dpframework02"
# NAME_SPACE = "dpframework02"
SITE_DN_FILE_NAME = "_site_dn.json"
MO_FILE_NAME = "_mo.json"
DEVICE_TYPE_LIST = ["20822", "20819", "20821", "20851"]


def send_request(url: str, query_body: dict):
    ip = os.popen(
        f'kubectl get svc -n {NAME_SPACE} | grep dpmodelproxyservice | sed -r "s/ +/,/g" | cut -d "," -f3').readlines()[0].strip()
    url = f"http://{ip}:8080{url}"

    response = requests.post(url, data=json.dumps(
        query_body), headers=HEADERS, verify=False)
    if str(response.status_code) != '200':
        raise SystemError(f'Invalid status code. response: {response.text}')
    response_dict: dict = json.loads(response.text)
    return response_dict


def generate_mo_query_body(company_dn, marker="0", limit=1):
    return {
        "moQueryCondition": {
            "values": {
                company_dn: [
                    {
                        "field": "mocId",
                        "operator": "in",
                        "values": DEVICE_TYPE_LIST
                    },
                    {
                        "field": "rootDevice",
                        "operator": "equal",
                        "values": ["true"]
                    }
                ]
            }
        },
        "moFieldSelector": {
            "selectSet": [
                "dn",
                "name",
                "parentDn",
                "status",
                "mocId",
            ]
        },
        "marker": marker,
        "limit": limit,
        "additionalCondition": {
            "containsAncestor": False,
            "strongConsistency": False
        }
    }


def generate_site_dn_query_body(company_dn, marker="0", limit=1):
    return {
        "moQueryCondition": {
            "values": {
                company_dn: [
                    {
                        "field": "mocId",
                        "operator": "in",
                        "values": ["20801"]
                    }
                ]
            }
        },
        "moFieldSelector": {
            "selectSet": [
                "dn",
            ]
        },
        "marker": marker,
        "limit": limit,
        "additionalCondition": {
            "containsAncestor": False,
            "strongConsistency": False
        }
    }


def generate_esn_query_body(ne_mo_list):
    return [{"dn": item["dn"], "signalList": [50012]} for item in ne_mo_list]


def get_mo(generate_req_body, company_dn) -> None:
    result_list = []
    query_body = generate_req_body(company_dn)
    response_dict = send_request(QUERY_API, query_body)
    print(f'  Total={response_dict["total"]}')

    limit = response_dict['total'] if response_dict['total'] <= BATCH_QUERY_LIMIT else BATCH_QUERY_LIMIT
    marker = 1
    query_cnt = 0
    current_amount = 0
    # print(QUERY_API)
    while current_amount < response_dict['total']:
        print(f'  > Round {query_cnt} marker={marker} limit={limit}')
        query_body = generate_req_body(company_dn, marker, limit)
        # print(query_body)
        response_dict = send_request(QUERY_API, query_body)
        # print(response_dict)
        if not response_dict.get('moMap', {}).get(company_dn):
            break
        result_list.extend(response_dict['moMap'][company_dn])
        # marker = response_dict.get('marker')
        # if not marker:
        #     print(f'return for marker is null')
        #     break
        current_amount += len(response_dict['moMap'][company_dn])
        # if current_amount >= response_dict['total']:
        #     print(f"  Got {response_dict['total']} records")
        #     break
        query_cnt += 1
        if query_cnt > MAX_QUERY_TIME_LIMIT:
            raise SystemError(
                f'Exceed max query time limit: {MAX_QUERY_TIME_LIMIT}')
        marker = marker + 1
    return result_list


def save_result(file_name, result_list):
    f = open(file_name, 'w')
    f.write(json.dumps(result_list, indent=4))
    f.close()


def load_record(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def progress(percent):
    width = 50
    print("%s %d%%\r" % (('%%-%ds' % width) %
          (int(width * percent / 100) * '='), percent), end="")
    if percent >= 100:
        print()
        sys.stdout.flush()


def get_site_dn_set(company_dn):
    print(f'> Get site dn list of {company_dn}')
    site_dn_set = set([item["dn"] for item in get_mo(
        generate_site_dn_query_body, company_dn)])
    return site_dn_set


def load_company_ne_list(company_dn, site_dn_set):
    print(f'> Get mo list')
    mo_list = get_mo(generate_mo_query_body, company_dn)
    if site_dn_set:
        ne_mo_list = [
            item for item in mo_list if item["parentDn"] in site_dn_set]
    else:
        ne_mo_list = mo_list
    print(f'> NE mo size={len(ne_mo_list)}')

    return ne_mo_list


def main():
    if (len(sys.argv) > 1):
        global NAME_SPACE
        global SITE_DN_FILE_NAME
        global MO_FILE_NAME
        NAME_SPACE = sys.argv[1]
        SITE_DN_FILE_NAME = NAME_SPACE + "_site_dn.json"
        MO_FILE_NAME = NAME_SPACE + "_mo.json." + time.strftime("%Y%m%d_%H%M%S", time.localtime())
    else:
        return

    input(NAME_SPACE)
    company_dn = "/"
    # company_dn = "NE=101273493"

    ne_mo_list = []

    site_dn_set = []
    # if os.path.exists(SITE_DN_FILE_NAME):
    #     site_dn_set = set(load_record(SITE_DN_FILE_NAME))
    # else:
    #     site_dn_set = get_site_dn_set(company_dn)
    #     save_result(SITE_DN_FILE_NAME, list(site_dn_set))

    # print(site_dn_set)

    tmpNeList = load_company_ne_list(company_dn, site_dn_set)
    ne_mo_list.extend(tmpNeList)

    print(f"> Save result to {MO_FILE_NAME}")
    save_result(MO_FILE_NAME, ne_mo_list)


if __name__ == '__main__':
    main()
