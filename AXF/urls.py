"""AXF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
'''
全局路由配置
'''
from django.conf.urls import url, include
from django.contrib import admin
from App import views


urlpatterns = [
    # host/admin/...   访问django默认站点管理页面
    url(r'^admin/', admin.site.urls),

    # host/axf/...     交由App.urls进行处理
    url(r'^axf/', include('App.urls', namespace='axf')),

    # host/    主页的访问交由views.home函数处理
    url(r'^$', views.home),
]
