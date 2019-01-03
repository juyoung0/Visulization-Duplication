from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^static/(?P<filename>\w+.*)$', views.sankey_overview, name='sankey_overview'),
    url(r'^sankeylist.html$', views.sankey_list, name='sankey_list'),
    url(r'^playback.html$', views.playback, name='playback'),
    url(r'^stat.html$', views.stat, name='stat'),
    url(r'^regroup.html$', views.regroup, name='regroup'),
    url(r'^regroup2.html$', views.regroup2, name='regroup2'),
    url(r'^gettime.html$', views.get_time, name='gettime'),
    url(r'^gettime3.html$', views.get_time3, name='gettime3'),
    url(r'^sequence.html$', views.sequence, name='sequence'),
]
