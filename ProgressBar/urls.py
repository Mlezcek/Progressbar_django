"""
URL configuration for DjangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib import admin
from django.urls import path
from . import views

from ProgressBar.views import progress_view, admin_panel, create_progress_bar

urlpatterns = [
    path('', views.create_progress_view, name='create_progress'),
    path('created/<str:admin_id>/', views.created_view, name='created'),
    path('admin-panel/<str:admin_id>/', views.admin_panel, name='admin_panel'),
    path('progress/<str:public_id>/', views.progress_view, name='progress'),
    path('delete-update/<str:admin_id>/', views.delete_update, name='delete_update'),
  path('api/progress/<uuid:public_id>/', views.progress_embed_api, name='progress_embed_api'),
path('api/progress/<str:public_id>/', views.progress_embed_api, name='progress_embed_api'),

]
