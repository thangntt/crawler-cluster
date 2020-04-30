from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class DomainConfigModel(Model):
    __table_name__ = 'domain_config'
    domain = columns.Text(primary_key=True, partition_key=True)
    kafka_topic = columns.Text(required=True)
    time_delay = columns.Integer(required=True)
    concurrent_user = columns.Integer(required=True, default=1)