import random
import re
import scrapy
from Spider.day10.lose_men.lose_men.items import LoseMenItem

headers = {
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "user-agent": str(random.randint(11111,111111)),
    "Referer": "https://www.baidu.com/s?ie=utf-8&f=1&rsv_bp=3&ch=&tn=baidu&bar=&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&oq=%E5%A4%B1%E4%BF%A1&rsv_pq=d17cefb70004ab37&rsv_t=9076vksDjJAhHFfah5i3aD5uppsf7X%2BNT4bgsHtJ7FwYDCHa5FwOs9tglEQ&rqlang=cn"
}
cookies= {
    "BIDUPSID":'DA765D9FB0170010EC2B5C1ABD6F375D',
    "PSTM":"1600162471",
    "BAIDUID":'DA765D9FB0170010095A2515BA651FCA:FG:1',
    "BDORZ":"B490B5EBF6F3CD402E515D22BCDA1598",
    "BDUSS":"3ZxZXJVc0pIaVV2em9mb29nRVNoNX5VLXFXU0ExN3ZBMm5XTmpPdGYyMmtEYWxmRVFBQUFBJCQAAAAAAAAAAAEAAADcDMPoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKSAgV-kgIFfT",
    "BDUSS_BFESS":"3ZxZXJVc0pIaVV2em9mb29nRVNoNX5VLXFXU0ExN3ZBMm5XTmpPdGYyMmtEYWxmRVFBQUFBJCQAAAAAAAAAAAEAAADcDMPoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKSAgV-kgIFfT",
    "BDRCVFR[feWj1Vr5u3D]":"I67x6TjHwwYf0",
    "delPer":"0",
    "PSINO":"2",
    "H_PS_PSSID":"32754_32617_1458_32792_31254_32230_7516_32117_31708_26350",
    "BA_HECTOR":"250k01ak80208l03o51foaruq0i"
}

class PoorMenSpider(scrapy.Spider):
    name = 'poor_men'
    # allowed_domains = ['poor_men.com']
    # start_urls = ['http://poor_men.com/']
    def start_requests(self):
        for page in range(1,5000,10):
            url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn={}&rn=10&from_mid=1&ie=utf-8&oe=utf-8&format=json&t=1601298935422&cb=jQuery1102033983800878092296_1601298923033&_=1601298923034".format(page)
            yield scrapy.Request(url,headers=headers,cookies=cookies)

    def parse(self, res):
        name_rule= '"iname":"(.*?)"'
        cardNum_rule = '"cardNum":"(.*?)"'
        areaName_rule = '"areaName":"(.*?)"'
        courtName_rule = '"courtName":"(.*?)"'
        gistId_rule = '"gistId":"(.*?)"'
        duty_rule = '"duty":"(.*?)"'
        performance_rule = '"performance":"(.*?)"'

        name = re.findall(name_rule,res.text)
        cardNum = re.findall(cardNum_rule,res.text)
        areaName = re.findall(areaName_rule,res.text)
        courtName = re.findall(courtName_rule,res.text)
        gistId = re.findall(gistId_rule,res.text)
        duty = re.findall(duty_rule,res.text)
        performance = re.findall(performance_rule,res.text)
        for i in name:
            index = name.index(i)
            item = LoseMenItem()
            item['name']= name[index]
            item['cardNum']=cardNum[index]
            item['areaName']=areaName[index]
            item['courtName']=courtName[index]
            item['gistId']=gistId[index]
            item['duty']=duty[index]
            item['performance']=performance[index]
            yield item

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy','crawl','poor_men'])