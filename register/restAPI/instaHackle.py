import random

import uuid

string4 = uuid.uuid4().hex[0:4]
string8 = uuid.uuid4().hex[0:8]
string12 = uuid.uuid4().hex[0:12]
string16 = uuid.uuid4().hex[0:16]
# print((uuid.uuid4().hex)[0:4])
device = "android-{}".format(string16)
var_uuid = uuid.uuid4().hex[0:32]
phone = "{}-{}-{}-{}-{}".format(string8, string4, string4, string4, string12)
guid = "{}-{}-{}-{}-{}".format(string8, string4, string4, string4, string12)
header = 'Connection: "close", "Accept": "*/*", "Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Cookie2": "$Version=1" "Accept-Language": "en-US", "User-Agent": "Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)"'
# var=$(curl -i -s -H "$header" https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup&guid=$uuid > /dev/null)
# var2=$(echo $var | grep -o 'csrftoken=.*' | cut -d ';' -f1 | cut -d '=' -f2)
# ig_sig="4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"
