from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, EXEC_PROFILE_GRAPH_DEFAULT, NoHostAvailable
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
from threading import Event
from crawler.config_properties import ConfigProperties
import ast


class CassandraConnectorSession:
    __config_properties = ConfigProperties.get_config()
    __username = __config_properties.get('cassandra', 'username')
    __password = __config_properties.get('cassandra', 'password')
    __hosts = ast.literal_eval(__config_properties.get('cassandra', 'hosts'))
    __default_keyspace = __config_properties.get('cassandra', 'default_keyspace')

    load_balancing_policy = TokenAwarePolicy(DCAwareRoundRobinPolicy())
    profile = ExecutionProfile(consistency_level=ConsistencyLevel.name_to_value['LOCAL_QUORUM'], load_balancing_policy=load_balancing_policy)

    auth_provider = PlainTextAuthProvider(username=__username, password=__password)
    cluster = Cluster(contact_points=__hosts, port=9042, auth_provider=auth_provider, idle_heartbeat_interval=200, execution_profiles={EXEC_PROFILE_DEFAULT: profile})
    session = cluster.connect(__default_keyspace)
