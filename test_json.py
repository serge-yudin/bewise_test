from random import randint
import json

import requests

query = {'questions_num': randint(1,4)}
headers = {'Content-type': 'application/json'}
url = 'http://localhost'


if __name__ == '__main__':
    res = requests.post(url, headers=headers, data=json.dumps(query))
    print(res.status_code)
    print(res.text)
