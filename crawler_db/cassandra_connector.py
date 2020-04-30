from cassandra.cqlengine.connection import setup
from cassandra.cqlengine.management import sync_table
from cassandra.auth import PlainTextAuthProvider
import logging
import ast
from crawler.config_properties import ConfigProperties
from crawler_db.url_crawl_model import UrlCrawlModel
from crawler_db.domain_config_model import DomainConfigModel


class CassandraConnector:
    __config_properties = ConfigProperties.get_config()
    __username = __config_properties.get('cassandra', 'username')
    __password = __config_properties.get('cassandra', 'password')
    __hosts = ast.literal_eval(__config_properties.get('cassandra', 'hosts'))
    __default_keyspace = __config_properties.get('cassandra', 'default_keyspace')

    auth_provider = PlainTextAuthProvider(username=__username, password=__password)
    setup(hosts=__hosts, default_keyspace=__default_keyspace, retry_connect=True, auth_provider=auth_provider)
    sync_table(UrlCrawlModel)
    sync_table(DomainConfigModel)
    logging.info("CassandraConnector initialed")

# a = CassandraConnector()
# print(a)
