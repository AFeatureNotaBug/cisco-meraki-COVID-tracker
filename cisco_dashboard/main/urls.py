from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ben', views.ben, name='ben'),
    path('fraser', views.fraser, name='fraser'),
    path('jake', views.jake, name='jake'),
    path('johnathan', views.johnathan, name='johnathan'),
    path('ruofan', views.ruofan, name='ruofan'),
    path('register', views.register, name="register"),
    path('login', views.user_login, name='login'),
    path('profile',views.profile,name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('<slug:name_slug>', views.showOrg, name = "show_org"),
]