'''
定义路由对应的处理函数
TODO name='xxx'究竟起何作用?
'''

from django.conf.urls import url
from App import views

urlpatterns = [

    # host/axf/home/...    交由views.home函数处理
    url(r'^home/', views.home, name='home'),

    # host/axf/market/     交由views.market函数处理
    url(r'^market/$', views.market, name='market'),

    # host/axf/market/一串数字/一串数字/一串数字/   交由views.marketWithParams函数处理
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.marketWithParams, name='marketWithParams'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^userregister/', views.user_register, name='user_register'),
    url(r'^userlogout/', views.user_logout, name='user_logout'),
    url(r'^userlogin/', views.user_login, name="user_login"),
    url(r'^checkuser/', views.check_user, name='check_user'),
    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^subtocart/', views.sub_to_cart, name='sub_to_cart'),
    url(r'^changecartstatus/', views.change_cart_status, name='change_cart_status'),
    url(r'^subcart/', views.sub_cart, name='sub_cart'),
    url(r'^addcart/', views.add_cart, name='add_cart'),
    url(r'^changecartselect/', views.change_cart_select, name='change_cart_select'),
    url(r'^generateorder/', views.generate_order, name="generate_order"),

    # orderinfo/一串数字/   交由views.order_info函数处理
    url(r'^orderinfo/(\d+)/', views.order_info, name="order_info"),
    url(r'^changeorderstatus/', views.change_order_status, name="change_order_status"),
    url(r'^orderlist/', views.order_list, name='order_list'),
    url(r'^orderlistwaitpay/', views.order_list_wait_pay, name='order_list_wait_pay'),
]