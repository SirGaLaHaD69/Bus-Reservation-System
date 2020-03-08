"""airline3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from airline3app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('index/<slug:pk>/',views.plane_detail_book,name='plane_detail_book'),
    path('airline3app/',include('airline3app.urls')),
    path('index/',views.index,name='index'),
    path('logout/',views.user_logout,name='user_logout'),
    path('payment/',views.payments_page,name='payments_page'),
    path('congrats/',views.congrats,name='congrats'),
    path('tickets/<int:pk>/remove/', views.DeleteTicketView.as_view(), name='ticket_remove'),
    path('tickets/',views.ticket_list,name='ticket_list'),
    path('tickets/<int:pk>/',views.my_tickets,name='my_tickets'),
]
