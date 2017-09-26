from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout, logout_then_login

urlpatterns = [
    #login and logout urls
    url(r'^login/$', views.User_login.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),

    #user profiles urls
    url(r'^users/$', views.UserList.as_view(template_name='account/user/user_list.html'), name='user_list'),
    #url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/(?P<slug>[-\w.]+)/$', views.UserDetail.as_view(template_name='account/user/user_detail.html'), name='user_detail'),
]
