import datetime
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib import messages
from django.http import HttpResponse
from lmsApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.models import Student, User, Userinterface_upload
def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    uploaded_img = Userinterface_upload.objects.all()

    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Library Managament System',
        'topbar' : True,
        'footer' : True,
        'uploaded_image': uploaded_img
    }

    return context
    
def userregister(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['uploaded_image'] = uploaded_img

    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

def save_register(request):
    uploaded_img = Userinterface_upload.objects.all()
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_profile(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            context['uploaded_image'] = uploaded_img

            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    uploaded_img = Userinterface_upload.objects.all()
    context['uploaded_image'] = uploaded_img
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

# Create your views here.
def login_page(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['uploaded_image'] = uploaded_img
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page'] = 'home3'
    context['page_title'] = 'Home3'
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all().count()
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag = 0, status = 1).all().count()
    context['students'] = Student.objects.filter(delete_flag = 0, status = 1).all().count()
    context['books'] = Student.objects.filter(delete_flag = 0, status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['transactions'] = models.Borrow.objects.all().count()
    context['uploaded_image'] = uploaded_img

    return render(request, 'home3.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    context['uploaded_image'] = uploaded_img

    return render(request,'profile.html', context)

@login_required
def users(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['uploaded_image'] = uploaded_img
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = User.objects.exclude(pk=request.user.pk).filter(is_superuser = False).all()
    return render(request, 'users.html', context)

@login_required
def save_user(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = User.objects.get(id = post['id'])
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_user(request, pk = None):
    uploaded_img = Userinterface_upload.objects.all()
    context['uploaded_image'] = uploaded_img
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = User.objects.get(id=pk)
    
    return render(request, 'manage_user.html', context)

@login_required
def delete_user(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def category(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['uploaded_image'] = uploaded_img

    context['page'] = 'category'
    context['page_title'] = "Category List"
    context['category'] = models.Category.objects.filter(delete_flag = 0).all()
    return render(request, 'category.html', context)

# @login_required
# def save_category(request):
#     resp = { 'status': 'failed', 'msg' : '' }
#     if request.method == 'POST':
#         post = request.POST
#         if not post['id'] == '':
#             category = models.Category.objects.get(id = post['id'])
#             form = forms.SaveCategory(request.POST, instance=category)
#         else:
#             form = forms.SaveCategory(request.POST) 

#         if form.is_valid():
#             form.save()
#             if post['id'] == '':
#                 messages.success(request, "Category has been saved successfully.")
#             else:
#                 messages.success(request, "Category has been updated successfully.")
#             resp['status'] = 'success'
#         else:
#             for field in form:
#                 for error in field.errors:
#                     if not resp['msg'] == '':
#                         resp['msg'] += str('<br/>')
#                     resp['msg'] += str(f'[{field.name}] {error}')
#     else:
#          resp['msg'] = "There's no data sent on the request"

#     return HttpResponse(json.dumps(resp), content_type="application/json")
def save_category(request):
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == "POST":
        print(request.POST)
        form = forms.SaveCategory(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"category created successfuly.")
            return redirect("category-page")

        else:
            messages.error(
                request, f"Somthing is not correct, please fill all fields correctly."
            )
    else:
        form = forms.SaveCategory()
    return render(request, "manage_category.html", {"form": form, 'uploaded_image':uploaded_img})


@login_required
def view_category(request, pk = None):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)
        context['uploaded_image']= uploaded_img
    return render(request, 'view_category.html', context)

# @login_required
# def manage_category(request, pk = None):
#     context = context_data(request)
#     context['page'] = 'manage_category'
#     context['page_title'] = 'Manage Category'
#     if pk is None:
#         context['category'] = {}
#     else:
#         context['category'] = models.Category.objects.get(id=pk)
    
    # return render(request, 'manage_category.html', context)
    
def manage_category(request, pk):
    uploaded_img = Userinterface_upload.objects.all()
    instance = get_object_or_404(models.Category, pk=pk)
    if request.method == "POST":
        form = forms.Category_update_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, "interface updated successfully.")
            return redirect("category-page")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.Category_update_form(instance=instance)
    return render( request,"manage_category.html",{"form": form, 'uploaded_image':uploaded_img})


def delete_category(request, pk):
    cate = models.Category.objects.all()
    for item in cate:
        if item.id == pk:    
            models.Category.delete()   
            messages.success(request, f"this file: {item.name} {item.status} has been deleted.")
    return redirect("category-page")

@login_required
def sub_category(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page'] = 'sub_category'
    context['page_title'] = "Sub Category List"
    context['uploaded_image'] = uploaded_img

    context['sub_category'] = models.SubCategory.objects.filter(delete_flag = 0).all()
    return render(request, 'sub_category.html', context)
    
def save_sub_category(request):
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == "POST":
        form = forms.SaveSubCategory(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(
                request, "subcategory has been created successfully.")
            return redirect("sub_category-page")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.SaveSubCategory()

    return render( request,"manage_sub_category.html",{"sub_category": form,'uploaded_image':uploaded_img})


def delete_sub_category(request, pk):
    cate = models.SubCategory.objects.all()
    for item in cate:
        if item.id == pk:    
            models.SubCategory.delete()   
            messages.success(request, f"this file: {item.name} {item.status} has been deleted.")
    return redirect("sub_category-page")


def manage_sub_category(request, pk):
    uploaded_img = Userinterface_upload.objects.all()
    instance = get_object_or_404(models.SubCategory, pk=pk)
    if request.method == "POST":
        form = forms.Sub_Category_update_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, "interface updated successfully.")
            return redirect("sub_category-page")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.Sub_Category_update_form(instance=instance)
    return render( request,"manage_sub_category.html",{"sub_category": form, 'uploaded_image':uploaded_img})
# @login_required
# def save_sub_category(request):
#     resp = { 'status': 'failed', 'msg' : '' }
#     if request.method == 'POST':
#         post = request.POST
#         if not post['id'] == '':
#             sub_category = models.SubCategory.objects.get(id = post['id'])
#             form = forms.SaveSubCategory(request.POST, instance=sub_category)
#         else:
#             form = forms.SaveSubCategory(request.POST) 

#         if form.is_valid():
#             form.save()
#             if post['id'] == '':
#                 messages.success(request, "Sub Category has been saved successfully.")
#             else:
#                 messages.success(request, "Sub Category has been updated successfully.")
#             resp['status'] = 'success'
#         else:
#             for field in form:
#                 for error in field.errors:
#                     if not resp['msg'] == '':
#                         resp['msg'] += str('<br/>')
#                     resp['msg'] += str(f'[{field.name}] {error}')
#     else:
#          resp['msg'] = "There's no data sent on the request"

#     return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
# def view_sub_category(request, pk = None):
#     context = context_data(request)
#     context['page'] = 'view_sub_category'
#     context['page_title'] = 'View Sub Category'
#     if pk is None:
#         context['sub_category'] = {}
#     else:
#         context['sub_category'] = models.SubCategory.objects.get(id=pk)
    
#     return render(request, 'view_sub_category.html', context)

# @login_required
# def manage_sub_category(request, pk = None):
#     context = context_data(request)
#     context['page'] = 'manage_sub_category'
#     context['page_title'] = 'Manage Sub Category'
#     if pk is None:
#         context['sub_category'] = {}
#     else:
#         context['sub_category'] = models.SubCategory.objects.get(id=pk)
#     context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all()
#     return render(request, 'manage_sub_category.html', context)

# @login_required
# def delete_sub_category(request, pk = None):
#     resp = { 'status' : 'failed', 'msg':''}
#     if pk is None:
#         resp['msg'] = 'Sub Category ID is invalid'
#     else:
#         try:
#             models.SubCategory.objects.filter(pk = pk).update(delete_flag = 1)
#             messages.success(request, "Sub Category has been deleted successfully.")
#             resp['status'] = 'success'
#         except:
#             resp['msg'] = "Deleting Sub Category Failed"

#     return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def books(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['uploaded_image']= uploaded_img
    context['books'] = models.Books.objects.filter(delete_flag = 0).all()
    return render(request, 'books.html', context)

def save_book(request):
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == "POST":
        form = forms.SaveBook(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Books has been created successfully.")
            return redirect("book-page")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.SaveBook()

    return render( request,"manage_book.html",{"book": form,'uploaded_image':uploaded_img})


def delete_book(request, pk):
    cate = models.Books.objects.all()
    for item in cate:
        if item.id == pk:    
            models.Books.delete()   
            messages.success(request, f"this file: {item.title} {item.status} has been deleted.")
    return redirect("manage-book")


def manage_book(request, pk):
    uploaded_img = Userinterface_upload.objects.all()
    instance = get_object_or_404(models.Books, pk=pk)
    if request.method == "POST":
        form = forms.Book_update_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, "interface updated successfully.")
            return redirect("manage-book")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.Book_update_form(instance=instance)
    return render( request,"manage_book.html",{"book": form, 'uploaded_image':uploaded_img})

@login_required
def borrows(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = context_data(request)
    context['page'] = 'borrow'
    context['page_title'] = "Borrowing Transaction List"
    context['uploaded_image'] = uploaded_img
    context['borrows'] = models.Borrow.objects.order_by('status').all()
    return render(request, 'borrows.html', context)

@login_required
def save_borrow(request):
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == 'POST':
        form = forms.SaveBorrow(request.POST) 
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Borrowing Transaction has been saved successfully.")
            return redirect("borrow-page")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.SaveBorrow()

    return render(request, 'manage_borrow.html', {'borrow': form, 'uploaded_image':uploaded_img})


@login_required
def manage_borrow(request, pk = None):
    uploaded_img = Userinterface_upload.objects.all()
    instance = get_object_or_404(models.Borrow, pk=pk)
    if request.method == "POST":
        form = forms.Borrow_update_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Transation updated successfully.")
            return redirect("borrow-page")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = forms.Borrow_update_form(instance=instance)
    return render( request,"manage_borrow.html",{"borrow": form, 'uploaded_image':uploaded_img})

@login_required
def delete_borrow(request, pk = None):
    cate = models.Borrow.objects.all()
    for item in cate:
        if item.id == pk:    
            models.Borrow.delete()   
            messages.success(request, f"this file: {item.title} {item.status} has been deleted.")
    return redirect("borrow-page")