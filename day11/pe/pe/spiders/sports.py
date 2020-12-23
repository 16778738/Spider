import scrapy


class SportsSpider(scrapy.Spider):
    name = 'sports'

    # allowed_domains = ['sports.com']
    # start_urls = ['http://sports.com/']
    def start_requests(self):
        # 单个队伍的球员的基本信息
        # url = "https://ziliaoku.sports.qq.com/cube/index?&cubeId=8&dimId=5&params=t1:3704,5007,5159,4651,1962937750,3818,4894,4750,1962937512,4480,4149,5678,5282,4300,1962938453,3835,1962938044,1962938514,1962938473,4720&from=sportsdatabase&callback="
        # 职业生涯信息
        url ="https://ziliaoku.sports.qq.com/cube/index?cubeId=10&dimId=31&params=t2:2019|t3:1|t4:13&from=sportsdatabase&callback="
        yield scrapy.Request(url)

    def parse(self, response):
        print(response.text)
        # 单个队伍的球员的基本信息
        # for i in response.json()['data']['playerBaseInfo']:
        #     print(i)
        list= response.json()['data']['nbaTeamPlayerSeasonStat']
        for i in list:
            index = list.index(i)

            assists = i['assists']# 助攻
            blocks = i['blocks'] # 盖帽
            defensiveRebounds = i['defensiveRebounds'] # 后场
            fgAttempted = i['fgAttempted']  #投篮次数
            fgMade =i['fgMade'] #进球次数
            points =i['points'] #得分
            threesMade =i['threesMade'] #三分进球数
            threesAttempted =i['threesAttempted'] #三分投球数
            rebounds = i['rebounds'] # 篮板

            print(i['blocks'])

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy','crawl','sports'])