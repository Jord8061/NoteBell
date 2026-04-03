import requests
import random
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

API_URL = "https://api2.openreview.net/notes"
FORUM_ID = "u5cSIeXVtK"

PARAMS = {
    "count": "true",
    "domain": "aclweb.org/ACL/ARR/2026/January",
    "forum": FORUM_ID
}

HEADERS = {
    "cookie": os.getenv("COOKIE"),
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "accept": "application/json,text/*;q=0.99",
}

FROM = "42211110@smail.swufe.edu.cn"
TO = {
    "1224145380@qq.com": "Jord",
    # "Jord8061@foxmail.com": "Jord",
    "xiaoyilin@whu.edu.cn": "Jeremy"
}

def make_header(email, name=None):
    return (name if name else email.split("@")[0]) + " <" + email + ">"

def send(subject, message, to=TO):
    if type(to) == dict:
        for k, v in to.items():
            send(subject, message, make_header(k, v))
        return
    if type(to) == list:
        for v in to:
            send(subject, message, make_header(v))
        return
    smtp = smtplib.SMTP()
    smtp.connect("smail.swufe.edu.cn", port=25)
    smtp.login(FROM, os.getenv("EMAIL_PASSWORD"))
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = make_header(FROM, "Jord")
    message['To'] = to
    message['Subject'] = Header(subject, 'utf-8')
    smtp.sendmail(FROM, to, message.as_string())

def solve():
    resp = requests.get(API_URL, PARAMS, headers=HEADERS, timeout=20)
    tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{tm}] status code:", resp.status_code)
    if resp.status_code != 200:
        print(f"[{tm}] request failed, retrying...")
        send(
            '「ACL」刚才的状态码是' + str(resp.status_code) + '，请检查！',
            'rt'
        )
        return 1
    data = resp.json()
    if data["count"] > 17:
        print(f"[{tm}] 好像出现了新的 note，可能是 Meta 更新了！")
        title = data["notes"][0]["content"].get("title", {}).get("value", "No Title")
        comment = data["notes"][0]["content"].get("comment", {}).get("value", "No Comment")
        send(
            '「ACL」出现了新的 note：' + title,
            comment + "\n\n链接：https://openreview.net/forum?id=" + FORUM_ID,
        )
        return 0
    print(f"[{tm}] 没有新的 note，继续监视...")
    send(
        '「喵喵喵」没有新的 note',
        '继续视奸ing...' + tm
    )
    return 1

# smtp = smtplib.SMTP()
# smtp.connect("smail.swufe.edu.cn", port=25)
# smtp.login(FROM, os.getenv("EMAIL_PASSWORD"))

while solve():
    time.sleep(random.randint(10, 20))