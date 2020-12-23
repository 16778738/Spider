# _*_coding:UTF-8 _*_
from urllib import request
import json

num = 1
for page in range(0, 120, 30):
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=6804522630827236065&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%98%BF%E7%8B%B8&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E9%98%BF%E7%8B%B8&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30".format(
        page)
    res = request.urlopen(url).read().decode("utf-8")
    for data in json.loads(res)['data']:
        if data:
            img_url = data['thumbURL']
            # 保存
            request.urlretrieve(img_url, filename="./img/" + str(num) + ".jpg")
            num += 1
