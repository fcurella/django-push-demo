### Installation

1. Create a virtualenv and download the project.
2. Install the requirements:

    $ pip install -r requirements.txt

### Running the project

    $ python manage.py run_gunicorn -c config/gunicorn

1. Open your browser at ``http://localhost:8000/``.
2. Open the javascript console.
3. Open a python interpreter (within your virtualenv).

To send a Server Side Event:

    >>> from django_sse.redisqueue import send_event
    >>> send_event('myevent', 'text')

To send a SocketIO packet from the server to the browser:

    >>> from myapp.utils import emit_to_channel
    >>> emit_to_channel('default_room', 'myevent', 'text')
 
To send a SocketIO packet from the browser to the server:

    > socket.emit('myevent', 'default_room', 'text')
