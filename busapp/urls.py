from django.urls import path
from airline3app import views

app_name = 'airline3app'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    path('fill_passenger/',views.passenger_info,name='passenger_info'),
]
