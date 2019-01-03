from django.conf.urls import include, url
from django.contrib import admin
from userstudy import views as user_view

urlpatterns = [
    # Examples:
    # url(r'^$', 'genovis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^genovis/', include('heatmap.urls', namespace="genovis")),
    url(r'^userstudy/', include('userstudy.urls', namespace="userstudy")),
]
