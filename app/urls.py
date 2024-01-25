from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.login, name='login'),
    path('level2/', views.Level2Auth.as_view(), name='level2'),
    path('level3/', views.Level3Auth.as_view(), name='level3'),
    path('resendOTP/', views.resendOTP, name='resend'),
    path('loggedin/', views.loggedIn, name='loggedin'),
    path('logout/', views.logoutUser, name='logout'),
    path('confirm/', views.UnBlockUser.as_view(), name='confirm'),
    re_path(r'^unblock/$', views.UnBlockUser.as_view(), name='unblock')
]
