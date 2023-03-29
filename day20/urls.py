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
from django.urls import path, include
from app02 import views
from app03.views import account_show, account_add, account_delete, account_edit, admin_list, admin_add, admin_edit, \
    admin_delete, admin_reset

urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    path('department/list/', views.department_list),
    path('add/', views.add),
    path('delete/', views.delete),
    path('department/add/', views.department_add),
    path('<int:uid>/edit/', views.department_edit),
    path('user/list/', views.user_list),
    path('user/<int:uid>/delete/', views.user_delete),
    path('user/add/', views.user_add),
    path('user/<int:uid>/edit/', views.user_edit),
    path('account/list/', account_show),
    path('account/add/', account_add),
    path('account/<int:uid>/delete/', account_delete),
    path('account/<int:uid>/edit/', account_edit),
    path('admin_user/list/', admin_list),
    path('admin_user/add/', admin_add),
    path('admin_user/<int:uid>/edit/', admin_edit),
    path('admin_user/<int:uid>/delete/', admin_delete),
    path('admin_user/<int:uid>/reset/', admin_reset),
    path('login/', views.login),
    path('logout/', views.logout),
    path('task/list/', views.task_list),
    path('task/add/', views.task_add),
    path('order/list/', views.order_list),
    path('order/add/', views.order_add),
    path('order/delete/', views.order_delete),
    path('order/detail/', views.order_detail),
    path('order/edit/', views.order_edit)

]
