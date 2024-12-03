from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, LoginView, LogoutView
)
from .views import (
    profile, profile_single, admin_panel,
    profile_update, change_password,
    LecturerListView, StudentListView,AppliedStudentListView,
    staff_add_view, edit_staff,edit_appliedstudent,parent_list,upload_list,upload_update,
    delete_staff, student_add_view, student_apply_view,applied_profile,applystudent_add_view,Login_view2,dashboard,dashboard2,
    edit_student, delete_student, ParentAdd, validate_username, register,upload_userinterface,delete_student_application,delete_upload
)
from .forms import EmailValidationOnForgotPassword
from .models import *

uploaded_img = Userinterface_upload.objects.all()

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('admin_panel/', admin_panel, name='admin_panel'),

    path('user_profile/', profile, name='user_profile'),
    path('profile/<int:id>/detail/', profile_single, name='profile_single'),
    path('applied_profile/<int:id>/detail/', applied_profile, name='applied_student_profile'),
    path('setting/', profile_update, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),

    path('lecturers/', LecturerListView.as_view(), name='lecturer_list'),
    path('lecturer/add/', staff_add_view, name='add_lecturer'),
    path('staff/<int:pk>/edit/', edit_staff, name='staff_edit'),
    path('lecturers/<int:pk>/delete/', delete_staff, name='lecturer_delete'),
    
    path('students/', StudentListView.as_view(), name='student_list'),
    path('application_students/', AppliedStudentListView.as_view(), name='applied_student_list'),
    path('student/add/', student_add_view, name='add_student'),
    path('applystudent/add/', applystudent_add_view, name='add_applystudent'),
    path('student/apply/', student_apply_view, name='applied_student'),
    path('student/<int:pk>/edit/', edit_student, name='student_edit'),
    path('appliedstudent/<int:id>/edit/', edit_appliedstudent, name='appliedstudent_edit'),

    path('students/<int:pk>/delete/', delete_student, name='student_delete'),
    path('appliedstudent/<int:pk>/delete/', delete_student_application, name='appliedstudent_delete'),


    path('parents/add/', ParentAdd.as_view(), name='add_parent'),
    path('parents_list/', parent_list, name='parentlist'),

    
    path('dashboard2/', dashboard, name='dashboard2'),
    path('statistics/', dashboard2, name='dashboard3'),


    path('ajax/validate-username/', validate_username, name='validate_username'),

    path('register1/', register, name='register1'),
    path('upload/', upload_userinterface, name='interface_upload'),
    path('upload_list/', upload_list, name='interface_list'),
    path('update_interface/<int:pk>', upload_update, name='interface_update'),
    path('delete_interface/<int:pk>/delete/', delete_upload, name='upload_delete'),



    # path('add-student/', StudentAddView.as_view(), name='add_student'),

    # path('programs/course/delete/<int:pk>/', course_delete, name='delete_course'),

    # Setting urls
    # path('profile/<int:pk>/edit/', profileUpdateView, name='edit_profile'),
    # path('profile/<int:pk>/change-password/', changePasswordView, name='change_password'),

    # ################################################################

    path('login2/', LoginView.as_view(template_name= 'login page.html'), name='login2'),
    path('login3/', Login_view2 , name='login3'),

    path('logout/', LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),

    # path('password-reset/', PasswordResetView.as_view(
    #     form_class=EmailValidationOnForgotPassword,
    #     template_name='registration/password_reset.html'
    # ),
    #      name='password_reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(
    #     template_name='registration/password_reset_done.html'
    # ),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    #     template_name='registration/password_reset_confirm.html'
    # ),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/', PasswordResetCompleteView.as_view(
    #     template_name='registration/password_reset_complete.html'
    # ),
    #      name='password_reset_complete')
    # ################################################################
]
