"""
URL configuration for leafdiseaseproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from leafapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('updateprofile',views.updateprofile,name='updateprofile'),
    path('prediction',views.prediction,name='prediction'),
    path('communityform',views.communityform,name='communityform'),
    path('discussionboard',views.discussionboard,name='discussionboard'),
    path('feedbackform',views.feedback,name='feedbackform'),
    path('powderyprecaution',views.powderyprequations,name='powderyprecaution'),
    path('rustprecaution',views.rustprequations,name='rustprecaution'),
    path('sendalert', views.sendalert, name='sendalert')
]
