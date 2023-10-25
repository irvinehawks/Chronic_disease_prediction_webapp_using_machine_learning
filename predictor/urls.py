from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    #AUTH VIEWS
    path('', views.landing, name="landing"),
    path('home/', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),

    # MODEL VIEWS
    path('heart', views.heart, name="heart"),
    path('diabetes', views.diabetes, name="diabetes"),
    path('breast', views.breast, name="breast"),
]
