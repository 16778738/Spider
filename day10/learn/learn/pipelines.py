# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LearnPipeline:
    def process_item(self, item, spider):
        with open('51_job.txt', 'a', encoding='utf-8') as w:
            w.write(item['job_names'] + ":" + item['com_names'] + "\n")
        return item
