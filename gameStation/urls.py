from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gameStation.views.home', name='home'),
    # url(r'^gameStation/', include('gameStation.foo.urls')),
    url(r'^$','principal.views.index'),
    url(r'^muestraNoticias/$', 'principal.views.muestraNoticias'),
   url(r'^recommendGame/$', 'principal.views.recommendGame'),
   url(r'^get_name/', 'principal.views.get_name', name='get_name'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
