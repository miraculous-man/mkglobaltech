from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, LoginView, LogoutView
)

urlpatterns = [
    path('login/', views.loginPage, name="login1"),
    path('logout/', views.logoutUser, name="logout1"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home2"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('login/', LoginView.as_view(template_name= 'base/login_register.html'), name='login'),

]
