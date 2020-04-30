from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class UrlCrawlModel(Model):
    __table_name__ = 'url_crawl'
    domain = columns.Text(primary_key=True, partition_key=True)
    url = columns.Text(primary_key=True)
    count_called = columns.TinyInt(primary_key=True, clustering_order='desc')
    create_time = columns.DateTime()
    header_request = columns.Text()
    type_handler = columns.TinyInt()


