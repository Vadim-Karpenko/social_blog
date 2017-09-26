from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.Article_create.as_view(), name='create'),
    url(r'^detail/(?P<pk>\d+)/$', views.DetailView.as_view(template_name='blog/article/article_detail.html'), name='detail'),
    url(r'^$', views.ListView.as_view(template_name='blog/article/list.html'), name='list_view'),
    #url(r'^delete/$', views.blog_delete, name='blog_delete'),
]
