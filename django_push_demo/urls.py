from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myapp import views

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
    url(r'^incr/$', views.incr, name='incr'),  # socket.io uses the well-known URL `/socket.io/` for its protocol
    url(r'^delete/$', views.delete, name='delete'),  # socket.io uses the well-known URL `/socket.io/` for its protocol
    url(r'^socket\.io', views.socketio_service, name='socketio_service'),  # socket.io uses the well-known URL `/socket.io/` for its protocol
    url(r'^$', views.HomePage.as_view(), name='homepage'),
)
urlpatterns += staticfiles_urlpatterns()
