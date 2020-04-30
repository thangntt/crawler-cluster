from crawler_db.cassandra_connector import CassandraConnector
from crawler_db.cassandra_connector_session import CassandraConnectorSession

def create_table_in_cassandra():
    ca = CassandraConnector()
    print(ca)

def fake_data():
    __session = CassandraConnectorSession.session
    __session.execute("INSERT INTO domain_config(domain, concurrent_user, kafka_topic, time_delay) values('gen.lib.rus.ec', 1, 'topic_1', 5)")
    __session.execute("INSERT INTO domain_config(domain, concurrent_user, kafka_topic, time_delay) values('libgen.me', 1, 'topic_2', 3)")

    __session.execute("INSERT INTO url_crawl(domain, count_called, create_time, header_request, type_handler, url) VALUES ('gen.lib.rus.ec', 0, toUnixTimestamp(now()), '', 1, 'http://gen.lib.rus.ec/search.php?&req=data&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page=1')")
    __session.execute("INSERT INTO url_crawl(domain, count_called, create_time, header_request, type_handler, url) VALUES ('gen.lib.rus.ec', 0, toUnixTimestamp(now()), '', 1, 'http://gen.lib.rus.ec/search.php?&req=data&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page=2')")
    __session.execute("INSERT INTO url_crawl(domain, count_called, create_time, header_request, type_handler, url) VALUES ('libgen.me', 0, toUnixTimestamp(now()), '', 1, 'https://libgen.lc/ads.php?md5=b88976015f46966d04b0e7e9c405d427&key=5363')")
    __session.execute("INSERT INTO url_crawl(domain, count_called, create_time, header_request, type_handler, url) VALUES ('libgen.me', 0, toUnixTimestamp(now()), '', 1, 'https://libgen.lc/ads.php?md5=1b88dcdcc771a2d145d7f1ac6b41dd2e&key=6339')")


if __name__ == '__main__':
    create_table_in_cassandra()
    fake_data()
    print('Done')