from django.conf.urls import url, include
from django.contrib import admin
from index import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cmdb/', include('cmdb.urls'), name='cmdb'),
    url(r'^$', views.index, name="index")
]
