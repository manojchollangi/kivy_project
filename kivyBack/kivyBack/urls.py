"""
URL configuration for kivyBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from backEndApi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-otp/', views.get_otp_to_mobile_number, name='get_otp'),
    path("signup/",views.user_creation,name="signup"),
    path("signout/",views.signout_view),
    path("users/",views.get_all_users,name="users"),
    path("signin/",views.signin_view,name='signin'),
]
