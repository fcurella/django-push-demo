from socketio.namespace import BaseNamespace
from myapp.utils import redis_connection
import json


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


class MyNamespaceThreadFriendly(BaseNamespace):
    rooms = set()

    def initialize(self):
        self.r = redis_connection().pubsub()

    def listener(self, room):
        self.r.subscribe(['socketio_%s' % room for room in self.rooms])

        for m in self.r.listen():
            if m['type'] == 'message':
                data = json.loads(m['data'])
                self.process_event(data)

    def on_subscribe(self, *args):
        for channel in args:
            self.join(channel)

    def join(self, room):
        """
        Kills the existing listener, and starts a new one subscribing to the new channel.
        """
        super(MyNamespaceThreadFriendly, self).join(room)
        self.rooms.add(room)
        if getattr(self, 'listener_greenlet', False):
            self.listener_greenlet.kill()

        self.listener_greenlet = self.spawn(self.listener, room)
        self.emit('joined', room)

    def on_myevent(self, *args):
        self.emit('myevent', *args)
