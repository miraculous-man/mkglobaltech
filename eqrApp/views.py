from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from eqrApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.models import Userinterface_upload, Student, User



def context_data():
    uploaded_img = Userinterface_upload.objects.all()

    context = {
        'page_name' : '',
        'page_title' : 'Chat Room',
        'system_name' : 'Employee ID with QR Code Generator',
        'topbar' : True,
        'footer' : True,
        'uploaded_image':uploaded_img
    }

    return context


# Create your views here.
# def login_page(request):
#     context = context_data()
#     context['topbar'] = False
#     context['footer'] = False
#     context['page_name'] = 'login'
#     context['page_title'] = 'Login'
#     return render(request, 'login.html', context)

# def login_user(request):
#     logout(request)
#     resp = {"status":'failed','msg':''}
#     username = ''
#     password = ''
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 resp['status']='success'
#             else:
#                 resp['msg'] = "Incorrect username or password"
#         else:
#             resp['msg'] = "Incorrect username or password"
#     return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['employees'] = models.Employee.objects.count()
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def employee_list(request):
    context =context_data()
    context['page'] = 'employee_list'
    context['page_title'] = 'Employee List'
    context['employees'] = models.Employee.objects.all()
    uploaded_img = Userinterface_upload.objects.all()
    context["uploaded_image"] =  uploaded_img

    return render(request, 'employee_list.html', context)

@login_required 
def manage_employee(request, pk=None):
    context =context_data()
    if pk is None:
        context['page'] = 'add_employee'
        context['page_title'] = 'Add New Employee'
        context['employee'] = {}
    else:
        context['page'] = 'edit_employee'
        context['page_title'] = 'Update Employee'
        context['employee'] = models.Employee.objects.get(id=pk)

    return render(request, 'manage_employee.html', context)

@login_required
def save_employee(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent into the request."

    else:
        if request.POST['id'] == '':
            form = forms.SaveEmployee(request.POST, request.FILES)
        else:
            employee = models.Employee.objects.get(id = request.POST['id'])
            form = forms.SaveEmployee(request.POST, request.FILES, instance = employee)
        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                messages.success(request, f"{request.POST['employee_code']} has been added successfully.")
            else:
                messages.success(request, f"{request.POST['employee_code']} has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")
                    resp['msg'] += str(f"[{field.label}] {error}")

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("Staff ID is Invalid")
    else:
        context = context_data()
        context['employee'] = User.objects.get(id=pk)
        context['uploaded_image'] = Userinterface_upload.objects.all()

        return render(request, 'view_id.html', context)
@login_required
def view_studentcard(request, pk =None):
    if pk is None:
        return HttpResponse("Student ID is Invalid")
    else:
        context = context_data()
        context['student'] = Student.objects.get(student__pk= pk)
        context['uploaded_image'] = Userinterface_upload.objects.all()

        return render(request, 'view_student_id.html', context)


@login_required
def view_scanner(request):
    context = context_data()
    return render(request, 'scanner.html', context)


@login_required
def user_idcard(request, pk = None):
    if pk is None:
        return HttpResponse("User code is Invalid")
    else:
        context = context_data()
        context['employee'] = User.objects.get(pk=pk)
        context['uploaded_image'] = Userinterface_upload.objects.all()

        return render(request, 'user_id.html', context)
    
@login_required
def view_details(request, pk = None):
    if pk is None:
        return HttpResponse("Staff code is Invalid")
    else:
        context = context_data()
        context['employee'] = User.objects.get(pk=pk)
        context['uploaded_image'] = Userinterface_upload.objects.all()

        return render(request, 'view_details.html', context)
@login_required
def id_details(request, pk):
    if id is None:
        return HttpResponse("Student code is Invalid")
    else:
        context = context_data()
        context['student'] = Student.objects.get(student__pk= pk)
        return render(request, 'id_details.html', context)

@login_required
def delete_employee(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = "No data has been sent into the request."
    else:
        try:
            models.Employee.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'Employee has been deleted successfully.')
        except:
            resp['msg'] = "Employee has failed to delete."

    return HttpResponse(json.dumps(resp), content_type="application/json")
