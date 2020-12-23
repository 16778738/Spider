import json
import random
import re

import requests
num = 46410
for page in range(46410,100000,10):
    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn={}&rn=10&from_mid=1&ie=utf-8&oe=utf-8&format=json&t=1601298935422&cb=jQuery1102033983800878092296_1601298923033&_=1601298923034".format(page)
    headers = {
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "user-agent": str(random.randint(11111,111111)),
        "cookie": "BIDUPSID=DA765D9FB0170010EC2B5C1ABD6F375D; PSTM=1600162471; BAIDUID=DA765D9FB0170010095A2515BA651FCA:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=2; H_PS_PSSID=32754_32617_1458_32792_7567_31254_32795_32230_7516_32117_31708_26350",
        "Referer": "https://www.baidu.com/s?ie=utf-8&f=1&rsv_bp=3&ch=&tn=baidu&bar=&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&oq=%E5%A4%B1%E4%BF%A1&rsv_pq=d17cefb70004ab37&rsv_t=9076vksDjJAhHFfah5i3aD5uppsf7X%2BNT4bgsHtJ7FwYDCHa5FwOs9tglEQ&rqlang=cn"
    }
    res = requests.get(url, headers=headers).content.decode('utf-8')

    name_rule= '"iname":"(.*?)"'
    cardNum_rule = '"cardNum":"(.*?)"'
    areaName_rule = '"areaName":"(.*?)"'
    courtName_rule = '"courtName":"(.*?)"'
    gistId_rule = '"gistId":"(.*?)"'
    duty_rule = '"duty":"(.*?)"'
    performance_rule = '"performance":"(.*?)"'

    name = re.findall(name_rule,res)
    cardNum = re.findall(cardNum_rule,res)
    areaName = re.findall(areaName_rule,res)
    courtName = re.findall(courtName_rule,res)
    gistId = re.findall(gistId_rule,res)
    duty = re.findall(duty_rule,res)
    performance = re.findall(performance_rule,res)
    for i in range(0,10):
        with open("失信人员名单.txt","a",encoding="utf-8") as w:
            w.write("失信人姓名:" + name[i] + " " + "身份证号:" + cardNum[i] + " " + "执行法院:" + courtName[i] + " " + "省份:" + areaName[i] + " " + "案号:" + gistId[i] + " " + "生效法律文书确定的义务:" + duty[i] + " " + "被执行人的履行情况:" + performance[i] + "\n")
            num += 1
    if num >=100000:
        break
    print(num)