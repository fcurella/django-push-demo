from django.conf import settings
from redis import Redis
from redis import ConnectionPool as RedisConnectionPool
from redis.connection import Connection
import json


WEBSOCKET_REDIS_BROKER_DEFAULT = {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0
}


CONNECTION_KWARGS = getattr(settings, 'WEBSOCKET_REDIS_BROKER', {})


class ConnectionPoolManager(object):
    """
    A singleton that contains and retrieves redis ``ConnectionPool``s according to the connection settings.
    """
    pools = {}

    @classmethod
    def key_for_kwargs(cls, kwargs):
        return ":".join([str(v) for v in kwargs.values()])

    @classmethod
    def connection_pool(cls, **kwargs):
        pool_key = cls.key_for_kwargs(kwargs)
        if pool_key in cls.pools:
            return cls.pools[pool_key]

        params = {
            'connection_class': Connection,
            'db': kwargs.get('DB', 0),
            'password': kwargs.get('PASSWORD', None),
            'host': kwargs.get('HOST', 'localhost'),
            'port': int(kwargs.get('PORT', 6379))
        }

        cls.pools[pool_key] = RedisConnectionPool(**params)
        return cls.pools[pool_key]


def redis_connection():
    """
    Returns a redis connection from one of our pools.
    """
    pool = ConnectionPoolManager.connection_pool(**CONNECTION_KWARGS)
    return Redis(connection_pool=pool)


def emit_to_channel(channel, event, *data):
    r = redis_connection()
    args = [channel] + list(data)
    r.publish('socketio_%s' % channel, json.dumps({'name': event, 'args': args}))
