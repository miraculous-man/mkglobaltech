from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from result.models import Result
from .decorators import lecturer_required, student_required, admin_required
from course.models import *
from result.models import TakenCourse
from app.models import Session, Semester
from .forms import StaffAddForm, StudentAddForm, ProfileUpdateForm, ParentAddForm, StudentApplicationForm,Userinterface_form,Userinterface_update_form
from .models import User, Student, Parent,StudentApplication, Userinterface_upload


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(
        username__iexact=username).exists()}
    return JsonResponse(data)


def register(request):
    if request.method == "POST":
        print(request.POST)
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created successfuly.")
            form = StudentAddForm()
        else:
            messages.error(
                request, f"Somthing is not correct, please fill all fields correctly."
            )
    else:
        form = StudentAddForm()
    return render(request, "./register.html", {"form": form})


def upload_userinterface(request):
    if request.method == "POST":
        print(request.POST,request.FILES)
        form = Userinterface_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created successfuly.")
            return redirect("interface_list")

        else:
            messages.error(
                request, f"Somthing is not correct, please fill all fields correctly."
            )
    else:
        form = Userinterface_form()
    return render(request, "interface_control.html", {"form": form})



def upload_list(request):

    context = Userinterface_upload.objects.all() 

    return render(request, "interface_list.html", {"content": context, 'uploaded_image':context})

def upload_update(request, pk):
    instance = get_object_or_404(Userinterface_upload, pk=pk)
    if request.method == "POST":
        form = Userinterface_update_form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, "interface updated successfully.")
            return redirect("interface_list")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = Userinterface_update_form(instance=instance)
    return render( request,"interface_update.html",{"form": form})


def delete_upload(request, pk):
    uploaded_file = get_object_or_404(Userinterface_upload, pk=pk)
    # full_name = student.user.get_full_name
    uploads = Userinterface_upload.objects.all()
    for item in uploads:
        if item.id == pk:    
            uploaded_file.delete()   
            messages.success(request, f"this file: {item.contact_us} {item.event_feed} has been deleted.")
    return redirect("interface_list")
# def student_apply(request):
#     if request.method == "POST":
#         form = StudentAddForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Account created successfuly.")
#         else:
#             messages.error(
#                 request, f"Somthing is not correct, please fill all fields correctly."
#             )
#     else:
#         form = StudentAddForm(request.POST)
#     return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    """Show profile of any user that fire out the request"""
    uploaded_img = Userinterface_upload.objects.all()
    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    if request.user.is_lecturer:
        courses = Course.objects.filter(
            allocated_course__lecturer__pk=request.user.id
        ).filter(semester=current_semester)
        return render(
            request,
            "accounts/profile.html",
            {
                "title": request.user.get_full_name,
                "courses": courses,
                "current_session": current_session,
                "current_semester": current_semester,
                "uploaded_image":uploaded_img
            },
        )
    elif request.user.is_student:
        level = Student.objects.get(student__pk=request.user.id)
        try:
            parent = Parent.objects.get(student=level)
        except:
            parent = "no parent set"
        courses = TakenCourse.objects.filter(
            student__student__id=request.user.id, course__level=level.level
        )
        context = {
            "title": request.user.get_full_name,
            "parent": parent,
            "courses": courses,
            "level": level,
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image":uploaded_img
        }
        return render(request, "accounts/profile.html", context)
    else:
        staff = User.objects.filter(is_lecturer=True)
        return render(
            request,
            "accounts/profile.html",
            {
                "title": request.user.get_full_name,
                "staff": staff,
                "current_session": current_session,
                "current_semester": current_semester,
                "uploaded_image":uploaded_img

            },
        )


@login_required
@admin_required
def profile_single(request, id):
    uploaded_img = Userinterface_upload.objects.all()
    """Show profile of any selected user"""
    if request.user.id == id:
        return redirect("/profile/")

    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    user = User.objects.get(pk=id)
    if user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(
            semester=current_semester
        )
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "Lecturer",
            "courses": courses,
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image": uploaded_img
        }
        return render(request, "accounts/profile_single.html", context)
    elif user.is_student:
        student = Student.objects.get(student__pk=id)
        courses = TakenCourse.objects.filter(
            student__student__id=id, course__level=student.level
        )
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "student",
            "courses": courses,
            "student": student,
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image": uploaded_img
        }
        return render(request, "accounts/profile_single.html", context)
    else:
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "superuser",
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image": uploaded_img
        }
        return render(request, "accounts/profile_single.html", context)


@login_required
@admin_required
def applied_profile(request, id):
    """Show profile of any selected user"""
    uploaded_img = Userinterface_upload.objects.all()
    if id:
        user = StudentApplication.objects.all()

        return render(request, "accounts/applied_student_profile.html",{'students':user,'pk':id, "uploaded_image":uploaded_img})


    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    if user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(
            semester=current_semester
        )
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "Lecturer",
            "courses": courses,
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image": uploaded_img
        }
        return render(request, "accounts/profile_single.html", context)
    elif user.is_student:
        student = Student.objects.get(student__pk=id)
        courses = TakenCourse.objects.filter(
            student__student__id=id, course__level=student.level
        )
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "student",
            "courses": courses,
            "student": student,
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image": uploaded_img
        }
        return render(request, "accounts/profile_single.html", context)
    else:
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "superuser",
            "current_session": current_session,
            "current_semester": current_semester,
            "uploaded_image": uploaded_img
        }
        return render(request, "accounts/applied_student_profile.html", context)


@login_required
@admin_required
def admin_panel(request):
    uploaded_img = Userinterface_upload.objects.all()

    return render(request, "setting/admin_panel.html", {'uploaded_image':uploaded_img})


# ########################################################


# ########################################################
# Setting views
# ########################################################
@login_required
def profile_update(request):
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated successfully.")
            return redirect("user_profile")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(
        request,
        "setting/profile_info_change.html",
        {
            "title": "Setting ",
            "form": form,
            "uploaded_image": uploaded_img
        },
    )


@login_required
def change_password(request):
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, "Your password was successfully updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error(s) below. ")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "setting/password_change.html",
        {
            "form": form,
            "uploaded_image": uploaded_img,

        },
    )


# ########################################################


@login_required
@admin_required
def staff_add_view(request):
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == "POST":
        form = StaffAddForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account for lecturer "
                + first_name
                + " "
                + last_name
                + " has been created.",
            )
            return redirect("lecturer_list")
    else:
        form = StaffAddForm()

    context = {
        "title": "Lecturer Add ",
        "form": form,
        "uploaded_image": uploaded_img
    }

    return render(request, "accounts/add_staff.html", context)


@login_required
@admin_required
def edit_staff(request, pk):
    uploaded_img = Userinterface_upload.objects.all()
    instance = get_object_or_404(User, is_lecturer=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, "Lecturer " +
                             full_name + " has been updated.")
            return redirect("lecturer_list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(
        request,
        "accounts/edit_lecturer.html",
        {
            "title": "Edit Lecturer ",
            "form": form,
            "uploaded_image":uploaded_img
        },
    )


@method_decorator([login_required, admin_required], name="dispatch")
class LecturerListView(ListView):
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/lecturer_list.html"
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lecturers | "
        uploaded_img = Userinterface_upload.objects.all()
        context["uploaded_image"] =  uploaded_img
        return context


# @login_required
# @lecturer_required
# def delete_staff(request, pk):
#     staff = get_object_or_404(User, pk=pk)
#     staff.delete()
#     return redirect('lecturer_list')


@login_required
@admin_required
def delete_staff(request, pk):
    lecturer = get_object_or_404(User, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, "Lecturer " + full_name + " has been deleted.")
    return redirect("lecturer_list")


# ########################################################


# ########################################################
# Student views
# ########################################################
@login_required
@admin_required
def student_add_view(request):
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == "POST":
        print(request.POST)
        form = StudentAddForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account for " + first_name + " " + last_name + " has been created.",
            )
            return redirect("student_list")
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = StudentAddForm()

    return render(
        request,
        "accounts/add_student.html",
        {"title": "Add Student ", "form": form, "uploaded_image":uploaded_img},
    )


def student_apply_view(request):
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            StudentApplicationForm( messages.success(
                request,
                "Account has been created successfuly. Addmission will be sent to you in 48hrs",
            ))
        else:
            messages.error(request, "Correct the error(s) below.")

    else:
        form = StudentApplicationForm()

    return render(
        request,
        "accounts/application_form.html",
        {"title": "Apply Student ", "form": form, "uploaded_image":uploaded_img}
    )


@login_required
@admin_required
def applystudent_add_view(request):
    uploaded_img = Userinterface_upload.objects.all()

    # {'csrfmiddlewaretoken': ['fDDcDlwaKkoLIZ7sJ46uT0HLljNEFnEnyCYBBkd5qbWQQkG5fa76YTUKflgv3wpf'], 'username': ['0003'], 'password1': ['12341234'], 'password2': ['12341234'], 'first_name': ['Blessing'], 'last_name': ['matter'], 'email': ['bleesing@gmail.com'], 'address': ['Agbada flow station2 igwuruta'], 'phone': ['08147345059'], 'department': ['1'], 'level': ['Bachloar']}
    form = StudentAddForm({'username': ['0006'], 'password1': ['12341234mi'], 'password2': ['12341234mi'], 'first_name': ['Joy'], 'last_name': ['matter'], 'email': ['bleesing@gmail.com'], 'address': ['Agbada flow station2 igwuruta'], 'phone': ['08147345059'], 'department': ['1'], 'level': ['Bachloar'],})
    first_name ='Joy'
    last_name = 'Joy'
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Account for " + first_name + " " + last_name + " has been created successfully.",
        )
        return redirect("student_list")
    else:
        messages.error(request, "Correct the error(s) below.")


    return render(
        request,
        "accounts/student_list.html",
        {"title": "Add Student ", "form": form, "uploaded_image": uploaded_img,
},
    )

@method_decorator([login_required, admin_required], name="dispatch")
class StudentListView(ListView):
    template_name = "accounts/student_list.html"
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        queryset = Student.objects.all()
        query = self.request.GET.get("student_id")
        if query is not None:
            queryset = queryset.filter(Q(department=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Students | DjangoSMS"
        uploaded_img = Userinterface_upload.objects.all()
        context["uploaded_image"] =  uploaded_img
        return context





@login_required
@admin_required
def edit_student(request, pk):
    # instance = User.objects.get(pk=pk)
    student = Student.objects.get(student__pk=pk)
    uploaded_img = Userinterface_upload.objects.all()
    instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
            
        if form.is_valid():
            form.save()

            messages.success(
                request, ("Student " + full_name + " has been updated."))
            return redirect("student_list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(
        request,
        "accounts/edit_student.html",
        {
            "title": "Edit-profile ",
            "form": form,
            "uploaded_image":uploaded_img
        },
    )


@login_required
@admin_required
def edit_appliedstudent(request,id):
    uploaded_img = Userinterface_upload.objects.all()

    instance = StudentApplication.objects.get(id=id)
    # instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = StudentApplicationForm(
            request.POST, request.FILES, instance=instance)
        full_name = instance.first_name
        if form.is_valid():
            form.save()

            messages.success(
                request, ("Student " + full_name + " has been updated."))
            return redirect("applied_student_list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = StudentApplicationForm(instance=instance)
    return render(
        request,
        "accounts/edit_appliedstudents.html",
        {
            "title": "Edit-profile | ",
            "form": form,
            "uploaded_image": uploaded_img,
        },
    )

@method_decorator([login_required, admin_required], name="dispatch")
class AppliedStudentListView(ListView):
    template_name = "accounts/applied_student.html"
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        queryset = StudentApplication.objects.all()
        query = self.request.GET.get("id")
        if query is not None:
            queryset = queryset.filter(Q(department=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uploaded_img = Userinterface_upload.objects.all()
        context["uploaded_image"] =  uploaded_img

        return context     



@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # full_name = student.user.get_full_name
    student.delete()
    messages.success(request, "Student has been deleted.")
    return redirect("student_list")


@login_required
@admin_required
def delete_student_application(request, pk):
    student = get_object_or_404(StudentApplication, pk=pk)
    # full_name = student.user.get_full_name
    students = StudentApplication.objects.all()
    for appliedstudent in students:
        if appliedstudent.id == pk:    
            student.delete()   
            messages.success(request, f"Student: {appliedstudent.first_name} {appliedstudent.last_name} has been deleted.")
    return redirect("applied_student_list")
# ########################################################


class ParentAdd(CreateView):
    model = Parent
    form_class = ParentAddForm
    template_name = "accounts/parent_form.html"



# def parent_add(request):
#     if request.method == 'POST':
#         form = ParentAddForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = ParentAddForm(request.POST)

@login_required
@admin_required
def parent_list(request):
    parents = Parent.objects.all()
    uploaded_img = Userinterface_upload.objects.all()

    return render(request,'accounts/parents_list.html',{"parent":parents, 'uploaded_image':uploaded_img})

def Login_view2(request):
    uploaded_img = Userinterface_upload.objects.all()

    return render(request,'login page.html',{'uploaded_image':uploaded_img})


def dashboard(request):
    uploaded_img = Userinterface_upload.objects.all()
    total_staff = User.objects.filter(is_lecturer= True).count()
    total_students = Student.objects.all().count()
    subjects = Course.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    attendance_list = Program.objects.all()
    applied_student = StudentApplication.objects.all().count()
    total_attendance = attendance_list.count()
    sessions = Session.objects.all().order_by('-is_current_session', '-session')
   
    students_all = Student.objects.all()
    attendance_list = []
    subject_list = []
    all_grade = []

    for item in students_all:
        my_students = Student.objects.get(student__pk=item.student.id)
        courses = TakenCourse.objects.filter(student__student__pk=item.student.id, course__level=my_students.level)
        results = Result.objects.filter(student__student__pk= item.student.id)
    
        # code to get session only
        for result in results:
            sessions = result.session

        
        grand_total = 0
        for course in courses:
            grand_total += course.total
            count = courses.count()
            if int(grand_total) == 0:
                grand_total = 0
                count = 0
                average = 0
                print(f'grand_total: {grand_total}')
            else:
                average = grand_total//count
                print(f'grand_total: {grand_total}')
    try:  
        print(f'subject: {course}')
        print(f'count {count}')

        if  average >= 90:
                grade = 'A_plus'
        elif average >= 85:
                grade = 'A'
        elif  average >= 80:
                grade = 'A'
        elif  average >= 70:
                grade = 'B'
        elif  average >= 60:
                grade = 'C'
        elif  average >= 50:
                grade = 'D'
        elif  average >= 40:
                grade = 'E'

        elif  average <= 39:
                grade = 'F'
        else:
                grade = 'failure'

        attendance_list.append(float(average))
        all_grade.append(grade)
        print(f'average: {attendance_list}')
        print(f'student_id: {item.student.id}')

        # for subject in subjects:
        #     attendance_count = Program.objects.all().count()
        #     attendance_list.append(attendance_count)

        # Total Subjects and students in Each Course
        course_all = Course.objects.all()
        course_name_list = []
        subject_count_list = []
        student_count_list_in_course = []

        for course in course_all:
            subjects = Course.objects.filter(id=course.id).count()
            students = Student.objects.all().count()
            course_name_list.append(course.title)
            subject_count_list.append(subjects)
            student_count_list_in_course.append(students)
        
        student_all = Student.objects.all()
        subject_list = []
        student_count_list_in_subject = []
        for student in student_all:
            student_count = Student.objects.all().count()
            subject_list.append(student.student.username)
            student_count_list_in_subject.append(student_count) 
        
            # courses = TakenCourse.objects.filter(student__student__pk=student.id, course__level=student.level)
            # grand_total = 0
            # count = 1
            
            # for course in courses:
            #     grand_total += course.total
            #     count += 1
            # average = grand_total//count
            # attendance_count = float(average) 
        # For Students
        student_attendance_present_list=[]
        student_attendance_leave_list=[]
        student_name_list=[]

        all_students = Student.objects.all()
        for studentss in all_students:  
            # attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
            # absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
            # leave = LeaveReportStudent.objects.filter(student_id=student.id, status=1).count()
            # student_attendance_present_list.append(attendance)
            # student_attendance_leave_list.append(leave+absent)
            student_name_list.append(studentss.level)
        for sessionss in sessions:
            sessions_year = sessionss
        # length_student = [i for i in range(1,len(all_students)+1) ]
        #(length_student)
   
        context = {
            'page_title': "Administrative Dashboard",
            'total_students': total_students,
            'total_staff': total_staff,
            'total_course': total_course,
            'total_subject': total_subject,
            'subject_list': subject_list,
            'attendance_list': attendance_list,
            'student_attendance_present_list': student_attendance_present_list,
            'student_attendance_leave_list': student_attendance_leave_list,
            "student_name_list": student_name_list,
            "student_count_list_in_subject": student_count_list_in_subject,
            "student_count_list_in_course": student_count_list_in_course,
            "course_name_list": course_name_list,
            "uploaded_image": uploaded_img,
            "applied_student_list": applied_student,
            "session_year": sessions,
            "students":all_students,
            "courses": courses,
            "result": result,
            "student": zip(all_students,attendance_list,all_grade),
            "grand_total": int(grand_total),
            "average": attendance_list,
            "session": sessions,
            "grade": grade

        }
    except UnboundLocalError:
        all_students = Student.objects.all()

        context = {
            'page_title': "Administrative Dashboard",
            'total_students': total_students,
            'total_staff': total_staff,
            'total_course': total_course,
            'total_subject': total_subject,
            'subject_list': subject_list,
            'attendance_list': 'none',
            'student_attendance_present_list': ['0','0','0','0'],
            'student_attendance_leave_list': ['0','0','0','0'],
            "student_name_list": ['0','0','0','0'],
            "student_count_list_in_subject": student_count_list_in_subject,
            "student_count_list_in_course": student_count_list_in_course,
            "course_name_list": course_name_list,
            "uploaded_image": uploaded_img,
            "applied_student_list": applied_student,
            "session_year": sessions_year,
            "students":all_students,
            "courses": 'no couse yet',
            "result": 'no result yet',
            "student": zip(all_students,['0','0','0','0'],['0','0','0','0']),
            "grand_total": int(grand_total),
            "average": 'none',
            "session": sessions,
            "grade": grade

        }
        

    return render(request,'Dashboard.html',context)
def dashboard2(request):
    uploaded_img = Userinterface_upload.objects.all()
    students = Student.objects.all()
    total_staff = User.objects.filter(is_lecturer= True).count()
    total_students = Student.objects.all().count()
    subjects = Course.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    attendance_list = Program.objects.all()
    applied_student = StudentApplication.objects.all().count()
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    # for subject in subjects:
    #     attendance_count = Program.objects.all().count()
    #     attendance_list.append(attendance_count)

    # Total Subjects and students in Each Course
    course_all = Course.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subjects = Course.objects.filter(id=course.id).count()
        students = Student.objects.all().count()
        course_name_list.append(course.title)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)
    
    student_all = Student.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for student in student_all:
        student_count = Student.objects.all().count()
        subject_list.append(student.student.username)
        student_count_list_in_subject.append(student_count) 
       

        courses = TakenCourse.objects.filter(student__student__pk=student.student.id, course__level=student.level)
        grand_total = 0
        counts = courses.count()
        
        for course in courses:
            grand_total += course.total
            average = grand_total//counts
        attendance_count = float(average) 
        attendance_list.append(attendance_count)
    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Student.objects.all()
    for student in students:
        
        # attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        # absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        # leave = LeaveReportStudent.objects.filter(student_id=student.id, status=1).count()
        # student_attendance_present_list.append(attendance)
        # student_attendance_leave_list.append(leave+absent)
        student_name_list.append(student.level)

    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'student_attendance_present_list': student_attendance_present_list,
        'student_attendance_leave_list': student_attendance_leave_list,
        "student_name_list": student_name_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "student_count_list_in_course": student_count_list_in_course,
        "course_name_list": course_name_list,
        "uploaded_image": uploaded_img,
        "applied_student_list": applied_student,


    }

    return render(request,'dashboard2.html',context)
