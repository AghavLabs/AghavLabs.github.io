#!/usr/bin/python

versionCode = '500418'
versionName = '5.4.18'

import os
import importlib

while True:
    for lib in ['requests', 'ntplib']:
        try:
            importlib.import_module(lib)
        except ModuleNotFoundError:
            os.system(f'pip install {lib}')
            break
    else:
        break

import requests, json, hashlib, urllib.parse, time, sys, os, base64, ntplib
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse, quote

version = "1.5.3"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(
    f"\n{CYAN}{BOLD}╔══════════════════════════════════════╗{RESET}\n"
    f"{CYAN}{BOLD}║{RESET}    {WHITE}{BOLD}[V{version}] For issues or feedback{RESET}   {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╠══════════════════════════════════════╣{RESET}\n"
    f"{CYAN}{BOLD}║   {RESET} {YELLOW}Mi Community Bootloader Tool{RESET}       {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╚══════════════════════════════════════╝{RESET}\n"
)

User = "okhttp/4.12.0"
headers = {"User-Agent": User}

def login():
    base_url = "https://account.xiaomi.com"
    sid = "18n_bbs_global"

    print(
        f"\n{CYAN}{BOLD}╔══════════════════════════════════════╗{RESET}"
        f"\n{CYAN}{BOLD}║{RESET}   {WHITE}{BOLD}     Mi Account LOGIN PANEL{RESET}        {CYAN}{BOLD}║{RESET}"
        f"\n{CYAN}{BOLD}╚══════════════════════════════════════╝{RESET}"
    )

    user = input(f"{YELLOW}➤ Enter Mi ID:{RESET} ")
    pwd = input(f"{YELLOW}➤ Enter Mi Pwd :{RESET} ")

    hash_pwd = hashlib.md5(pwd.encode()).hexdigest().upper()
    cookies = {}

    def parse(res):
        return json.loads(res.text[11:])

    r = requests.get(f"{base_url}/pass/serviceLogin", params={'sid': sid, '_json': True}, headers=headers, cookies=cookies)
    cookies.update(r.cookies.get_dict())

    deviceId = cookies["deviceId"]

    data = {k: v[0] for k, v in parse_qs(urlparse(parse(r)['location']).query).items()}
    data.update({'user': user, 'hash': hash_pwd})

    r = requests.post(f"{base_url}/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)
    cookies.update(r.cookies.get_dict())
    res = parse(r)

    if res["code"] == 70016: exit("invalid user or pwd")

    region = json.loads(requests.get(
        "https://account.xiaomi.com/pass/user/login/region",
        headers=headers,
        cookies=cookies
    ).text[11:])["data"]["region"]

    nonce, ssecurity = res['nonce'], res['ssecurity']
    res['location'] += f"&clientSign={quote(base64.b64encode(hashlib.sha1(f'nonce={nonce}&{ssecurity}'.encode()).digest()))}"

    serviceToken = requests.get(res['location'], headers=headers, cookies=cookies).cookies.get_dict()

    micdata = {
        "userId": res['userId'],
        "new_bbs_serviceToken": serviceToken["new_bbs_serviceToken"],
        "region": region,
        "deviceId": deviceId
    }

    with open("micdata.json", "w") as f:
        json.dump(micdata, f)

    return micdata

try:
    with open('micdata.json') as f:
        micdata = json.load(f)
except:
    micdata = login()

new_bbs_serviceToken = micdata["new_bbs_serviceToken"]
deviceId = micdata["deviceId"]
region = micdata['region']

print(f"\nAccount Region: {region}\n")

api = "https://sgp-api.buy.mi.com/bbs/api/global/"

U_state = api + "user/bl-switch/state"
U_apply = api + "apply/bl-auth"
U_info = api + "user/data"

headers = {
  'User-Agent': User,
  'Content-Type': "application/json",
  'Cookie': f"new_bbs_serviceToken={new_bbs_serviceToken};versionCode={versionCode};versionName={versionName};deviceId={deviceId};"
}

info = requests.get(U_info, headers=headers).json()['data']

print(f"Community Days: {info['registered_day']}")
print(f"Level: {info['level_info']['level']}")
print(f"Points: {info['level_info']['current_value']}")

def state_request():
    state = requests.get(U_state, headers=headers).json().get("data", {})

    if state.get("is_pass") == 1:
        exit("Unlock access already granted")

state_request()

def apply_request():
    apply = requests.post(U_apply, data=json.dumps({"is_retry": True}), headers=headers)

    if apply.json().get("code") != 0:
        exit(apply.json())

    print("Application sent successfully.")

apply_request()
