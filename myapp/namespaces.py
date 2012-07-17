from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin
from myapp.utils import redis_connection
import json


class MyNamespace(BaseNamespace, RoomsMixin):
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
        super(MyNamespace, self).join(room)
        self.spawn(self.listener, room)
        self.emit('joined', room)

    def on_myevent(self, room, *args):
        self.emit_to_room(room, 'myevent', *args)

    def emit_to_room(self, room, event, *args):
        """
        This is almost the same as ``.emit_to_room()`` on the parent class,
        but it sends the event only over the current socket.

        This is to avoid a problem when there are more client than workers, and
        a single message can get delivered multiple times.
        """
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)

        if 'rooms' not in self.socket.session:
            return
        if room_name in self.socket.session['rooms']:
            self.socket.send_packet(pkt)


class MyNamespaceThreadFriendly(MyNamespace):
    rooms = set()

    def initialize(self):
        self.r = redis_connection().pubsub()

    def listener(self, room):
        self.r.subscribe(['socketio_%s' % room for room in self.rooms])

        for m in self.r.listen():
            if m['type'] == 'message':
                data = json.loads(m['data'])
                self.process_event(data)

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
