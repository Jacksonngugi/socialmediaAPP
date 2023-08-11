from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('signup/signin',views.signin,name='signin'),
    path('signin/signup',views.signup,name='signup'),
    path('setting/',views.setting,name='setting'),
    path('signin/setting',views.setting,name='setting'),
    path('signin/index.html/',views.index,name='index')
]