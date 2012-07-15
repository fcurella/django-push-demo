# Create your views here.
from django.views.generic import TemplateView
from django_sse.redisqueue import RedisQueueView

from socketio import socketio_manage
from myapp.namespaces import MyNamespace


class HomePage(TemplateView):
    template_name = 'index.html'


class SSE(RedisQueueView):
    pass


def socketio_service(request):
    socketio_manage(request.environ, namespaces={'': MyNamespace}, request=request)

    return {}
