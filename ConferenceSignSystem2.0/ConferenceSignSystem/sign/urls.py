from django.conf.urls import url
from sign import views_interface,views_sec_interface

app_name='sign'
urlpatterns=[
    # 对外提供的接口
    # ex: /api/add_event/
    url('^add_event/',views_interface.add_event, name='add_event'),
    # ex: /api/add_guest/
    url('^add_guest/',views_interface.add_guest, name='add_guest'),
    # ex: /api/get_event_list/
    url('^get_event_list/',views_interface.get_event_list, name='get_event_list'),
    # ex: /api/get_guest_list/
    url('^get_guest_list/',views_interface.get_guest_list, name='get_guest_list'),
    # ex: /api/user_sign/
    url('^user_sign/',views_interface.user_sign, name='user_sign'),
    # http basic 认证的接口
    # ex：/api/sec_add_event/
    url('^sec_add_event/',views_sec_interface.sec_add_event, name='sec_add_event'),
    # ex: /api/sec_add_guest/
    url('^sec_add_guest/', views_sec_interface.sec_add_guest, name='sec_add_guest'),
    # ex: /api/sec_get_event_list/
    url('^sec_get_event_list/', views_sec_interface.sec_get_event_list, name='sec_get_event_list'),
    # ex: /api/sec_get_guest_list/
    url('^sec_get_guest_list/', views_sec_interface.sec_get_guest_list, name='sec_get_guest_list'),
    # ex: /api/sec_user_sign/
    url('^sec_user_sign/', views_sec_interface.sec_user_sign, name='sec_user_sign'),
]


# fix bug: 不使用正则^，会导致sec_app_event被app_event覆盖