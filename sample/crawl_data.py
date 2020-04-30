from scrapy.crawler import CrawlerProcess
from crawler.kafka_spider import KafkaSpider
from crawler.url_info_pb2 import UrlInfoMessage
import logging.config


class CrawlData(KafkaSpider):
    topic = ['topic_1']
    group_id = 'topic_1'
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100
    }
    num_message_from_kafka = 1
    payload = UrlInfoMessage

    def parse(self, response):
        # get meta that put in request, see create request in kafka_spider.py
        logger.info(response.meta)
        logger.info('get body -->' + str(response.body))


logging.config.fileConfig('../config/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
})
process.crawl(CrawlData)
process.start()
logger.info("======================>DONE<========================")