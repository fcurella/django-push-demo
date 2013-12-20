from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from myapp.utils import redis_connection
import json


@namespace('')
class MyNamespace(BaseNamespace):
    def listener(self, room):
        r = redis_connection().pubsub()
        r.subscribe('socketio_%s' % room)

        for m in r.listen():
            if m['type'] == 'message':
                data = json.loads(m['data'])
                self.process_event(data)

    def on_subscribe(self, *args):
        for channel in args:
            self.join(channel)

    def join(self, room):
        """
        Spawn a listener and notifies the client that joining has been successful.

        Note that we spawn a listener (and thus, a new redis connection) for every room we join
        I've tried to spawn just once, but calling ``redis.listen()`` without a ``redis.subscribe()``
        causes the listener loop to exit immediately.
        """
        self.spawn(self.listener, room)
        self.emit('joined', room)

    def on_myevent(self, *args):
        self.emit('myevent', *args)

