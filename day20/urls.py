"""day20 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from app02 import views
from app03.views import admin_list, admin_add, admin_edit, \
    admin_delete, admin_reset

urlpatterns = [
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    path('department/list/', views.department_list),
    path('department/delete/', views.department_delete),
    path('department/add/', views.department_add),
    path('department/edit/', views.department_edit),
    path('department/detail/', views.department_detail),
    path('user/list/', views.user_list),
    path('user/<int:uid>/delete/', views.user_delete),
    path('user/add/', views.user_add),
    path('user/<int:uid>/edit/', views.user_edit),
    path('admin_user/list/', admin_list),
    path('admin_user/add/', admin_add),
    path('admin_user/<int:uid>/edit/', admin_edit),
    path('admin_user/<int:uid>/delete/', admin_delete),
    path('admin_user/<int:uid>/reset/', admin_reset),
    path('login/', views.login),
    path('logout/', views.logout),
    path('order/list/', views.order_list),
    path('order/add/', views.order_add),
    path('order/delete/', views.order_delete),
    path('order/detail/', views.order_detail),
    path('order/edit/', views.order_edit),
    path('register/', views.register),
    path('verify/', views.verify),
    path('customer/list/', views.customer_list),
    path('customer/add/', views.customer_add),
    path('customer/<int:uid>/edit/', views.customer_edit),
    path('customer/<int:uid>/delete/', views.customer_delete),

]
