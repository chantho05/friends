from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home), 
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout), 
    url(r'^friends$', views.friends),
    url(r'^add$', views.add),
    url(r'^remove$', views.remove),
    url(r'^user/1$', views.user),
    url(r'^otheruser/10$', views.otheruser),

]