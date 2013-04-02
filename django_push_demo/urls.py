from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myapp import views

import socketio.sdjango

socketio.sdjango.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_push_demo.views.home', name='home'),
    # url(r'^django_push_demo/', include('django_push_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^sse_incr/$', views.sse_incr, name='sse_incr'),
    url(r'^sse_delete/$', views.sse_delete, name='see_delete'),
    url(r'^sse/$', views.SSE.as_view(), name='sse'),
    url(r'^$', views.HomePage.as_view(), name='homepage'),
)
urlpatterns += staticfiles_urlpatterns()
