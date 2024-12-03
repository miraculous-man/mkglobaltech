from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Student, Parent, ApplyingStudent,StudentApplication,Userinterface_upload


class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'username', 'email', 'is_active', 'is_student', 'is_lecturer', 'is_parent', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_lecturer', 'is_parent', 'is_staff']

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class ParentAdmin(admin.ModelAdmin):
    list_display = [  'user','phone','student','relation_ship',
        'first_name', 'last_name', 'phone', 'email',]
   

class UserinterfaceAdmin(admin.ModelAdmin):
    list_display = [ 'news_feed','picture','contact_us','event_feed']

# class ScoreAdmin(admin.ModelAdmin):
#     list_display = [
#         'student', 'course', 'assignment', 'mid_exam', 'quiz',
#         'attendance', 'final_exam', 'total', 'grade', 'comment'
#     ]

class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'address', 'phone', 'email', 'date_of_birth',
        'LG_origin', 'state_origin', 'parent_name', 'parent_adress', 'parent_number',
        'emergency_contact', 'emergency_number', 'emergency_address', 'relationship',
        'level', 'department', 'student_files', 'student_certificate_waec_image',
        'student_certificate_jamb_image', 'student_certificate_other_image', 'student_passport'
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Parent, ParentAdmin)
admin.site.register(ApplyingStudent)
admin.site.register(StudentApplication,StudentAdmin)
admin.site.register(Userinterface_upload,UserinterfaceAdmin)

# admin.site.unregister(Group)
