#!/usr/bin/python
# Instagram Account Maker
# by Behdad Ahmadi
# Twitter: behdadahmadi
# https://github.com/behdadahmadi
# https://logicalcoders.com
import re

import requests
import hmac
import hashlib
import random
import string
import json
import argparse


def HMAC(text):
    key = '3f0a7d75e094c7385e3dbaa026877f2e067cbd1a4dbcf3867748f6b26f257117'
    hash = hmac.new(key.encode('utf-8'), msg=text.encode('utf-8'), digestmod=hashlib.sha256)
    return hash.hexdigest()


def randomString(size):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def __collect_sockets():
    sockets = []
    r = requests.get("https://www.sslproxies.org/")
    matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
    revised_list = [m1.replace("<td>", "") for m1 in matches]
    for socket_str in revised_list:
        sockets.append(socket_str[:-5].replace("</td>", ":"))

    return sockets


def create(username, name, email, password, sockets):
    current_socket = sockets.pop(0)
    getHeaders = {
        'User-Agent': 'Instagram 7.1.1 Android (21/5.0.2; 480dpi; 1080x1776; LGE/Google; Nexus 5; hammerhead; hammerhead; en_US)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1'}

    s = requests.Session()
    s.get('https://instagram.com', headers=getHeaders)
    guid = randomString(8) + '-' + randomString(4) + "-" + randomString(4) + '-' + randomString(4) + '-' + randomString(
        12)
    device_id = 'android-' + str(HMAC(str(random.randint(1000, 9999))))[0:min(64, 16)]
    information = {'username': username, 'first_name': name, 'password': password, 'email': email,
                   'device_id': device_id, 'guid': guid}
    js = json.dumps(information)
    payload = {'signed_body': HMAC(js) + '.' + js, 'ig_sig_key_version': '4'}
    postHeaders = {'Host': 'i.instagram.com',
                   'User-Agent': 'Instagram 7.1.1 Android (21/5.0.2; 480dpi; 1080x1776; LGE/Google; Nexus 5; hammerhead; hammerhead; en_US)',
                   'Accept-Language': 'en-US',
                   'Accept-Encoding': 'gzip',
                   'Cookie2': '$Version=1',
                   'X-IG-Connection-Type': 'WIFI',
                   'X-IG-Capabilities': 'BQ=='
                   }
    proxies = {"http": "http://" + current_socket, "https": "https://" + current_socket}

    x = s.post('https://i.instagram.com/api/v1/accounts/create/', headers=postHeaders, data=payload, proxies=proxies)

    result = json.loads(x.content)
    print(result)
    if result['status'] != 'fail':
        print(result)
        if result['account_created'] == True:
            print('Account has been created successfully')
        else:
            print('Error:')
            for i in result['errors']:
                print(str(result['errors'][i][0]))
    else:
        # if result['spam'] == True:

        print('Instagram blocks your IP due to spamming behaviour.')


if __name__ == '__main__':
    create('oddsFashionColins2', 'Colin\'s Styling ', 'mail23dsf@mail.com', '8989323846q', sockets=__collect_sockets())
