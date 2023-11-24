"""web URL Configuration

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
from django.urls import path
from app import views
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page),

    # enterance links
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_page, name='signup'),

    # user account links
    path('accounts/', include('django.contrib.auth.urls'), name='account'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('personalAccount/', views.personalAccount_page),
    path('personalAccount/personalAccountTemplates/<name>/', views.personalAccountTemplates_page, name='personalAccountTemplate'),


    # partner links
    path('partners/', views.partners_page, name='partners_page'),
    path('service/', views.service_page, name='service_page'),
    path('service/serviceTemplates/<name>/', views.serviceTemplate_page, name='serviceTemplate_page'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

