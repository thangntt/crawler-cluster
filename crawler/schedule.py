from crawler_db.cassandra_connector_session import CassandraConnectorSession
from crawler.kafka_producer_consumer import KafkaProducer
from crawler.url_info_pb2 import UrlInfoMessage
import time
import uuid
import logging.config

class Schedule:
    __session = CassandraConnectorSession.session
    __session.default_fetch_size = 1000
    __domain_configs = []
    __kafka_producer = KafkaProducer()

    def push_url_to_kafka(self):
        self.get_domain_config()
        next_time = int(time.time())
        domain_length = len(self.__domain_configs)

        while True:
            i = 0
            while i < domain_length:
                domain_config = self.__domain_configs[i]
                if domain_config['next_time'] < next_time:
                    SQL = "SELECT * FROM url_crawl WHERE domain='{}' limit {}".format(domain_config['domain'], domain_config['concurrent_user'])
                    datas = self.__session.execute(SQL)
                    for data in datas:
                        # send message to kafka,
                        message = UrlInfoMessage(url=data.url, uuid=str(uuid.uuid1()))
                        self.__kafka_producer.send_message(topic=domain_config['kafka_topic'], message=message)

                    domain_config['next_time'] = int(time.time()) + domain_config['time_delay']
                    self.__domain_configs[i] = domain_config

                # update next_time for next handler
                next_time = int(time.time())
                i += 1

    def get_domain_config(self):
        current_time = int(time.time())
        SQL = 'SELECT * FROM domain_config'
        future = self.__session.execute_async(SQL)
        datas = future.result()
        for data in datas:
            r = {}
            r['domain'] = data.domain
            r['kafka_topic'] = data.kafka_topic
            r['time_delay'] = data.time_delay
            r['concurrent_user'] = data.concurrent_user
            r['next_time'] = current_time
            self.__domain_configs.append(r)
        if future.has_more_pages:
            future.start_fetching_next_page()

if __name__ == '__main__':
    logging.config.fileConfig('../config/logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info("======================>BEGIN<========================")
    Schedule().push_url_to_kafka()
