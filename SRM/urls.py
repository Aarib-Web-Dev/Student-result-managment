"""
URL configuration for SRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from RMS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index ,name= 'index' ),
    path('login', views.Admin_login ,name= 'admin_login' ),
    path('dashboard', views.admin_dashboard ,name= 'admin_dashboard' ),
    path('create_class', views.create_class ,name= 'create_class' ),
    path('logout', views.Logout ,name= 'logout' ),
    path('manage_class', views.manage_class ,name= 'manage_class' ),
    path('edit_class/<int:id>/', views.edit_class, name='edit_class'),
    path('create_subject', views.create_subject, name='create_subject'),
    path('manage_subject', views.manage_subject, name='manage_subject'),
    path('edit_subject/<int:id>/', views.edit_subject, name='edit_subject'),
    path('create_subject_combination', views.create_subject_combination, name='create_subject_combination'),
    path('manage_subject_combination', views.manage_subject_combination, name='manage_subject_combination'),
    path('create_student', views.create_student, name='create_student'),
    path('manage_student', views.manage_student, name='manage_student'),
    path('create_result', views.create_result, name='create_result'),
    path('manage_result', views.manage_result, name='manage_result'),
    path('create_notice', views.create_notice, name='create_notice'),
    path('manage_notice', views.manage_notice, name='manage_notice'),
    path('change_password', views.change_password, name='change_password'),
]
