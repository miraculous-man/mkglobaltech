from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.decorators import admin_required, lecturer_required
from .forms import SessionForm, SemesterForm, NewsAndEventsForm, Contact_us_infoForm
from .models import *
from accounts.models import Userinterface_upload,User
from django.contrib.auth import authenticate, login, logout


# ########################################################
# News & Events
# ########################################################
def home_page_view(request):
    # items = NewsAndEvents.objects.all().order_by('-updated_date')
    uploaded_img = Userinterface_upload.objects.all()
    length_database = [i for i in range(1,len(uploaded_img)+1) ]
    
    def image_view():
        for i in range(1,len(uploaded_img)+1):
            if i == len(length_database):
                length_database = length_database
        return length_database        
        
    image_view
    # for id in range(1,len(uploaded_img)):
 

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=name)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=name, password=password)
        if request.user.is_authenticated:
            return redirect('home2')
        
        if user is not None:
            login(request, user)
            return redirect('home2')
        else:
            messages.error(request, 'Username OR password does not exit')
            return redirect('login1')

    return render(request, 'home.html',{'uploaded_image':uploaded_img, 'uploaded_image_zip':zip(uploaded_img, length_database) ,'ids':length_database})

@login_required
def home_view(request):
    items = NewsAndEvents.objects.all().order_by('-updated_date')
    uploaded_img = Userinterface_upload.objects.all()

    context = {
        'title': "News & Events ",
        'items': items,
        'uploaded_image':uploaded_img
    }
    return render(request, 'app/index.html', context)

@login_required
def contact(request):
    uploaded_img = Userinterface_upload.objects.all()
    length_database = [i for i in range(1,len(uploaded_img)+1) ]
         
    if request.method == 'POST':
        form = Contact_us_infoForm(request.POST)
        name = request.POST.get('name')
        if form.is_valid():
            form.save()

            messages.success(request, (name + ' your message has been successfuly sent.'))
            return redirect('contact_us')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = Contact_us_infoForm()
    return render(request, 'contact_us.html', {
        'title': 'Add Post',
        'form': form,
        'uploaded_image':uploaded_img, 'uploaded_image_zip':zip(uploaded_img, length_database) ,'ids':length_database
    })
def subscribers_messages(request):

    context = Contact_us_info.objects.all() 
    uploaded_img = Userinterface_upload.objects.all()

     
    return render(request, "message_list.html", {"content": context, 'uploaded_image':uploaded_img})

def delete_message(request, pk):
    massages = get_object_or_404(Contact_us_info, pk=pk)
    # full_name = student.user.get_full_name
    uploads = Contact_us_info.objects.all()
    for item in uploads:
        if item.id == pk:    
            messages.delete()   
            messages.success(request, f"this file: {item.name} {item.email} has been deleted.")
    return redirect("contact_us")
        
@login_required
def post_add(request):
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == 'POST':
        form = NewsAndEventsForm(request.POST)
        title = request.POST.get('title')
        if form.is_valid():
            form.save()

            messages.success(request, (title + ' has been uploaded.'))
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = NewsAndEventsForm()
    return render(request, 'app/post_add.html', {
        'title': 'Add Post | DjangoSMS',
        'form': form,
        'uploaded_image':uploaded_img
    })


@login_required
@lecturer_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == 'POST':
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get('title')
        if form.is_valid():
            form.save()

            messages.success(request, (title + ' has been updated.'))
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(request, 'app/post_add.html', {
        'title': 'Edit Post | DjangoSMS',
        'form': form,
        'uploaded_image':uploaded_img
    })


@login_required
@lecturer_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + ' has been deleted.'))
    return redirect('home')

# ########################################################
# Session
# ########################################################
@login_required
@lecturer_required
def session_list_view(request):
    """ Show list of all sessions """
    uploaded_img = Userinterface_upload.objects.all()
    sessions = Session.objects.all().order_by('-is_current_session', '-session')
    return render(request, 'app/session_list.html', {"sessions": sessions,'uploaded_image':uploaded_img})


@login_required
@lecturer_required
def session_add_view(request):
    """ check request method, if POST we add session otherwise show empty form """
    uploaded_img = Userinterface_upload.objects.all()
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_session')  # returns string of 'True' if the user selected Yes
            print(data)
            if data == 'true':
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, 'Session added successfully. ')
            return redirect('session_list')

    else:
        form = SessionForm()
    return render(request, 'app/session_update.html', {'form': form, 'uploaded_image':uploaded_img})


@login_required
@lecturer_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        data = form.data.get('is_current_session')
        if data == 'true':
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Session updated successfully. ')
                return redirect('session_list')
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, 'Session updated successfully. ')
                return redirect('session_list')

    else:
        form = SessionForm(instance=session)
    return render(request, 'app/session_update.html', {'form': form, 'uploaded_image':uploaded_img})


@login_required
@lecturer_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if session.is_current_session:
        messages.error(request, "You cannot delete current session")
        return redirect('session_list')
    else:
        session.delete()
        messages.success(request, "Session successfully deleted")
    return redirect('session_list')
# ########################################################


# ########################################################
# Semester
# ########################################################
@login_required
@lecturer_required
def semester_list_view(request):
    uploaded_img = Userinterface_upload.objects.all()

    semesters = Semester.objects.all().order_by('-is_current_semester', '-semester')
    return render(request, 'app/semester_list.html', {"semesters": semesters,'uploaded_image':uploaded_img})


@login_required
@lecturer_required
def semester_add_view(request):
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_semester')  # returns string of 'True' if the user selected Yes
            if data == 'True':
                semester = form.data.get('semester')
                ss = form.data.get('session')
                session = Session.objects.get(pk=ss)
                try:
                    if Semester.objects.get(semester=semester, session=ss):
                        messages.error(request, semester + " semester in " + session.session + " session already exist")
                        return redirect('add_semester')
                except:
                    semesters = Semester.objects.all()
                    sessions = Session.objects.all()
                    if semesters:
                        for semester in semesters:
                            if semester.is_current_semester == True:
                                unset_semester = Semester.objects.get(is_current_semester=True)
                                unset_semester.is_current_semester = False
                                unset_semester.save()
                        for session in sessions:
                            if session.is_current_session == True:
                                unset_session = Session.objects.get(is_current_session=True)
                                unset_session.is_current_session = False
                                unset_session.save()

                    new_session = request.POST.get('session')
                    set_session = Session.objects.get(pk=new_session)
                    set_session.is_current_session = True
                    set_session.save()
                    form.save()
                    messages.success(request, 'Semester added successfully.')
                    return redirect('semester_list')

            form.save()
            messages.success(request, 'Semester added successfully. ')
            return redirect('semester_list')
    else:
        form = SemesterForm()
    return render(request, 'app/semester_update.html', {'form': form, 'uploaded_image':uploaded_img})


@login_required
@lecturer_required
def semester_update_view(request, pk):
    semester = Semester.objects.get(pk=pk)
    uploaded_img = Userinterface_upload.objects.all()

    if request.method == 'POST':
        if request.POST.get('is_current_semester') == 'True': # returns string of 'True' if the user selected yes for 'is current semester'
            unset_semester = Semester.objects.get(is_current_semester=True)
            unset_semester.is_current_semester = False
            unset_semester.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()
            new_session = request.POST.get('session')
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                set_session = Session.objects.get(pk=new_session)
                set_session.is_current_session = True
                set_session.save()
                form.save()
                messages.success(request, 'Semester updated successfully !')
                return redirect('semester_list')
        else:
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                form.save()
                return redirect('semester_list')

    else:
        form = SemesterForm(instance=semester)
    return render(request, 'app/semester_update.html', {'form': form, 'uploaded_image':uploaded_img})


@login_required
@lecturer_required
def semester_delete_view(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if semester.is_current_semester:
        messages.error(request, "You cannot delete current semester")
        return redirect('semester_list')
    else:
        semester.delete()
        messages.success(request, "Semester successfully deleted")
    return redirect('semester_list')
# ########################################################


# from django.shortcuts import render_to_response
# from django.template import RequestContext

# def handler404(request, exception, template_name="common/404.html"):
#     response = render_to_response("common/404.html")
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render_to_response('common/500.html', {}, context_instance=RequestContext(request))
#     response.status_code = 500

#     return response


# def handler400(request, exception, template_name="common/400.html"):
#     response = render_to_response('common/400.html', context_instance=RequestContext(request))
#     response.status_code = 400

#     return response

@login_required
@admin_required
def dashboard_view(request):
    uploaded_img = Userinterface_upload.objects.all()
    context = {'uploaded_image':uploaded_img}
    return render(request, 'app/dashboard.html',context)