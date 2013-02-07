from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('ioestu.views',
	url(r'^$','index'),
	url(r'^logged/$','logged'),
    # Examples:
    # url(r'^$', 'ioests.views.home', name='home'),
    # url(r'^ioests/', include('ioests.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
urlpatterns = patterns('ioestu.endofday',
	url(r'^endofday/$', 'notificationTrigger'),
	)