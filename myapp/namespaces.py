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
        self.emit_to_room_with_echo(room, 'myevent', *args)

    def emit_to_room_with_echo(self, room, event, *args):
        """
        This is almost the same as ``.emit_to_room()`` on the parent class,
        but it doesn't exclude the current session from receiving the event.
        """
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'rooms' not in socket.session:
                continue
            if room_name in socket.session['rooms']:  # This is the only line different from ``.emit_to_room()``
                socket.send_packet(pkt)
