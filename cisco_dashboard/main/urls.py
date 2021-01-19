from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('overview', views.overview, name='overview'),
    
    path('register', views.register, name="register"),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('profile',views.profile,name='profile'),
    path('usedemokey',views.usedemokey),
    path('editapikey',views.editapikey),
    path('edit_scanning_api_url',views.edit_scanning_api_url),
    path('accounts/login/',views.user_login,name='login'),
    
]
