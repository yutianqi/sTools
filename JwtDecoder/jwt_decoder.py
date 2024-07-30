#!/usr/bin/env python

import json
import base64
import sys


def base64url_decode(base64_str):
    size = len(base64_str) % 4
    if size == 2:
        base64_str += '=='
    elif size == 3:
        base64_str += '='
    elif size != 0:
        raise ValueError('Invalid base64 string')
    return base64.urlsafe_b64decode(base64_str.encode('utf-8'))


def parse_jwt(jwt_token):
    jwt_token_list = jwt_token.split('.')
    header = base64url_decode(jwt_token_list[0]).decode()
    payload = base64url_decode(jwt_token_list[1]).decode()
    return {
        'header': json.loads(header),
        'payload': json.loads(payload),
        'signature': jwt_token_list[-1]
    }


if __name__ == '__main__':
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = input("jwt: ")
    if not token:
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZXRob2QiOiJHRVQiLCJhcHBJZCI6IlZPRC1TZXJ2aWNlUm91dGluZyIsInVyaSI6Ii92MS4wLzE5OTAzY2UxM2JiYjQyOGJiMmZlY2UxNDYwMjk5NjUzL2NzL3dvcmtmbG93L2RldGFpbHMiLCJqdGkiOiJiYzRlYzFlOS01MzhiLTQ4MDQtYTZhNy03MjkxZWM0ZTVkOTYiLCJpYXQiOjE3MjIzMTgzMDcsImV4cCI6MTcyMjMxODYwN30.3z2KnyNOwP1DuyI7pK_aLPqbwsd-bvfrI2VApEvw6cg'
    print(json.dumps(parse_jwt(token), indent=4))

