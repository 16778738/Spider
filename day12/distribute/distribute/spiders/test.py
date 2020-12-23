import scrapy
from scrapy_redis.spiders import RedisSpider


class TestSpider(RedisSpider):
    name = 'test'
    redis_key = 'testRedis:url'

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'test'])
