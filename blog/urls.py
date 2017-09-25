from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.Article_create.as_view(), name='create'),
    url(r'^detail/(?P<pk>\d+)/$', views.Detail.as_view(template_name='blog/article/detail.html'), name='detail'),
    #url(r'^$', views.blog_list, name='list'),
    #url(r'^delete/$', views.blog_delete, name='blog_delete'),
]
