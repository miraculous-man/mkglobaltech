from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('employee_list',views.home),
    # path('login2',views.login_page,name='login-page'),
    # path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    # path('logout1',views.logout_user,name='logout_user'),
    path('',views.employee_list,name='employee-page'),
    path('add_employee',views.manage_employee,name='add-employee'),
    path('edit_employee/<int:pk>',views.manage_employee,name='edit-employee'),
    path('save_employee',views.save_employee,name='save-employee'),
    path('view_card/<int:pk>',views.view_card,name='view-card'),
    path('view_idcard/<int:pk>',views.user_idcard,name='user-card'),

    path('view_details/<str:pk>',views.view_details,name='view-details'),
    path('id_details/<int:pk>',views.id_details,name='id-details'),
    path('view_student_card/<int:pk>',views.view_studentcard,name='view-studentcard'),


    path('view_details',views.view_details,name='scanned-code'),
    path('scanner',views.view_scanner,name='view-scanner'),
    path('delete_employee/<int:pk>',views.delete_employee,name='delete-employee'),
]
