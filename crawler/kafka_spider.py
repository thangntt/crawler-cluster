import scrapy
from scrapy import signals
import logging
from crawler.protobuf_message_handler import ProtobufMessageHandler
from scrapy.exceptions import DontCloseSpider
from crawler.kafka_producer_consumer import KafkaConsumer
from crawler.proxy_handler import ProxyHandler


class KafkaSpider(scrapy.Spider):
    __logger = logging.getLogger(__name__)
    topic = None
    group_id = None
    payload = None
    num_message_from_kafka = 1

    def __init__(self):
        if self.group_id is None:
            raise Exception('group_id is None')
        if self.topic is None:
            raise Exception('topic is None')
        if self.payload is None:
            raise Exception('payload is None')

        self.kafka_consumer = KafkaConsumer(self.group_id, self.topic)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.get_message_from_kafka()
        raise DontCloseSpider

    def get_message_from_kafka(self):
        try:
            msgs = self.kafka_consumer.consumer.consume(num_messages=self.num_message_from_kafka)
            for msg in msgs:
                if msg is None:
                    continue
                elif not msg.error():
                    self.__logger.info('topic: {}, partition: {}, offset: {}'.format(msg.topic(), msg.partition(), msg.offset()))
                    # convert message protobuf to object
                    message_deserialize = ProtobufMessageHandler.deserialize(msg.value(), self.payload)
                    req = scrapy.Request(url=message_deserialize.url, callback=self.parse)

                    # transfer all field to response, through meta
                    fields = self.payload.DESCRIPTOR.fields_by_name
                    for field in fields:
                        req.meta[field] = getattr(message_deserialize, field)

                    # check proxy exists
                    proxy_url = message_deserialize.proxy_url
                    if proxy_url is None or 'http' not in proxy_url or not ProxyHandler.contains(proxy_url):
                        proxy_url = ProxyHandler.random_proxy()
                    if proxy_url is not None and 'http' in proxy_url:
                        req.meta['proxy'] = proxy_url

                    self.crawler.engine.crawl(req, spider=self)
                elif msg.error() is not None:
                    self.__logger.error(msg.error().str())
                else:
                    self.__logger.error(msg.error().str())
        except Exception as e:
            self.__logger.error(e)

