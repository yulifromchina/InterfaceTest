from django.conf.urls import url
from sign import views_interface

app_name='sign'
urlpatterns=[
    # 对外提供的接口
    # ex: /api/add_event/
    url('add_event/',views_interface.add_event, name='add_event'),
    # ex: /api/add_guest/
    url('add_guest/',views_interface.add_guest, name='add_guest'),
    # ex: /api/get_event_list/
    url('get_event_list/',views_interface.get_event_list, name='get_event_list'),
    # ex: /api/get_guest_list/
    url('get_guest_list/',views_interface.get_guest_list, name='get_guest_list'),
    # ex: /api/user_sign/
    url('user_sign/',views_interface.user_sign, name='user_sing'),
]