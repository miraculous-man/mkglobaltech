from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from datetime import datetime
from course.models import Program
# from .models import User, Student, LEVEL
from .models import *

time = datetime.now()
class StaffAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Username", )

    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="First Name", )

    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Last Name", )

    address = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Address", )

    phone = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Mobile No.", )

    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Email", )
    dob = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'label':"Birthday"
            }
        ),
        required=True)
   
    gender = forms.ChoiceField(choices=[("Male","Male"), ("Female","Female")], label="Gender")


    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password Confirmation", )

    class Meta(UserCreationForm.Meta):
        model = User

    # @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        user.dob = self.cleaned_data.get('dob')
        user.gender = self.cleaned_data.get('gender')
        if commit:
            user.save()
        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'username_id'
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Last name",
    )

    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                'class': 'browser-default custom-select form-control',
            }
        ),
    )

    department = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={'class': 'browser-default custom-select form-control'}),
        label="Department",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label="Email Address",
    )
    dob = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'label':"Birthday"
            }
        ),
        required=True)
   
    gender = forms.ChoiceField(choices=[("Male","Male"), ("Female","Female")], label="Gender")
    switch = forms.ChoiceField(choices=[("True","True"), ("False","False")], label="Allow result")


    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password Confirmation", )
    

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    # @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.dob = self.cleaned_data.get('dob')
        user.gender = self.cleaned_data.get('gender')
        user.switch = self.cleaned_data.get('switch')
     

        user.save()
        student = Student.objects.create(
            student=user,
            level=self.cleaned_data.get('level'),
            department=self.cleaned_data.get('department'),
            switch = self.cleaned_data.get('switch')

        )
        student.save()
        return user


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'type': 'email', 'class': 'form-control', }),
        label="Email Address", )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', }),
        label="First Name", )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', }),
        label="Last Name", )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', }),
        label="Phone No.", )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', }),
        label="Address / city", )
    
    dob = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'label':"Birthday"
            }
        ),
        required=True)
    gender = forms.ChoiceField(choices=[("Male","Male"), ("Female","Female")], label="Gender")
    switch = forms.ChoiceField(choices=[("True","True"), ("False","False")], label="Allow result")


    class Meta:
        model = User
        fields = ['email', 'phone', 'address',
                  'picture', 'first_name', 'last_name', 'gender','dob','switch']
   
class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-mail address. "
            self.add_error('email', msg)
            return email


class ParentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Last name",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label="Email Address",
    )

    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(
            attrs={'class': 'browser-default custom-select form-control'}),
        label="Student",
    )

    relation_ship = forms.CharField(
        widget=forms.Select(
            choices=RELATION_SHIP,
            attrs={'class': 'browser-default custom-select form-control', }
        ),
    )

    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password Confirmation", )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

  #  @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.dob = self.cleaned_data.get('dob')
        user.gender = self.cleaned_data.get('gender')
        user.date_added = self.cleaned_data.get('date_added')
        user.date_created = self.cleaned_data.get('date_created')
        user.save()
        parent = Parent.objects.create(
            user=user,
            student=self.cleaned_data.get('student'),
            relation_ship=self.cleaned_data.get('relation_ship')
        )
        parent.save()
        return user


class StudentApplicationForm(forms.ModelForm):
  
    date_of_birth = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'label':"Birthday"
            }
        ),
        required=True)
    class Meta:
        model = StudentApplication
        fields = ('first_name','last_name','address','phone','email','date_of_birth',
                  'LG_origin','state_origin','parent_name','parent_adress','parent_number',
                  'emergency_contact','emergency_number','emergency_address','relationship',
                  'level','department', 'student_files', 'student_certificate_waec_image',
                  'student_certificate_jamb_image', 'student_certificate_other_image','student_passport')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control',  'type': 'date'})
        self.fields['LG_origin'].widget.attrs.update({'class': 'form-control'})
        self.fields['state_origin'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_adress'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_contact'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['relationship'].widget.attrs.update({'class': 'form-control'})
        self.fields['level'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_files'].widget.attrs.update( {'class': 'form-control'})
        self.fields['student_certificate_waec_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_certificate_jamb_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_certificate_other_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_passport'].widget.attrs.update(
            {'class': 'form-control'})


class AppliedStudentProfileUpdateForm(UserChangeForm):
    date_of_birth = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'label':"Birthday"
            }
        ),
        required=True)
    class Meta:
        model = StudentApplication
        fields = ('first_name','last_name','address','phone','email','date_of_birth',
                  'LG_origin','state_origin','parent_name','parent_adress','parent_number',
                  'emergency_contact','emergency_number','emergency_address','relationship',
                  'level','department', 'student_files', 'student_certificate_waec_image',
                  'student_certificate_jamb_image', 'student_certificate_other_image','student_passport')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control',  'type': 'date'})
        self.fields['LG_origin'].widget.attrs.update({'class': 'form-control'})
        self.fields['state_origin'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_adress'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_contact'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['relationship'].widget.attrs.update({'class': 'form-control'})
        self.fields['level'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_files'].widget.attrs.update( {'class': 'form-control'})
        self.fields['student_certificate_waec_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_certificate_jamb_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_certificate_other_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_passport'].widget.attrs.update(
            {'class': 'form-control'})


class StudentApplyForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'username_id'
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Last name",
    )

    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                'class': 'browser-default custom-select form-control',
            }
        ),
    )

    department = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={'class': 'browser-default custom-select form-control'}),
        label="Department",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label="Email Address",
    )
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        label="Date Of Birth",
    )
    LG_origin = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="L.G.A of Orign",
    )
    state_origin = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="State of Origin",
    )
    parent_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Name of Parent/Sponsor",
    )
    parent_adress = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address of Parent/Sponsor",
    )
    Parent_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Phone Number:",
    )

    Emergency_contact = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Persons to be contacted in case of emergenct",
    )
    relationship = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Relationship",
    )
    emergency_address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address of the person",
    )
    emergency_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Phone Number:",
    )

    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Password Confirmation", )

    file = forms.FileField(
        allow_empty_file=True, label="Student Documents")
    updated_date = forms.DateField(label= "Date") 
    upload_time = forms.TimeField(label= "Time")
    student_certificate_waec_image = forms.ImageField(
        allow_empty_file=True, label="WAEC CERTIFICATE IMAGE")
    student_certificate_jamb_image = forms.ImageField(
        allow_empty_file=True, label="JAMB CERTIFICATE IMAGE")
    student_certificate_other_image = forms.ImageField(
        allow_empty_file=True, label="OTHERS CERTIFICATE IMAGE")
    date_of_birth = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'label':"Birthday"
            }
        ),
        required=True)
    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    # @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.dob = self.cleaned_data.get('dob')
        user.gender = self.cleaned_data.get('gender')
        user.date_added = self.cleaned_data.get('date_added')
        user.date_created = self.cleaned_data.get('date_created')
        user.save()
        student = ApplyingStudent.objects.create(
            student=user,
            level=self.cleaned_data.get('level'),
            department=self.cleaned_data.get('department'),
            date_of_birth = self.cleaned_data.get('date_of_birth'),
            LG_origin = self.cleaned_data.get('LG_origin'),
            state_origin = self.cleaned_data.get('state_origin'),
            parent_name = self.cleaned_data.get('parent_namet'),
            parent_adress = self.cleaned_data.get('parent_adress'),
            Parent_number = self.cleaned_data.get('Parent_number'),
            Emergency_contact = self.cleaned_data.get('Emergency_contact'),
            relationship = self.cleaned_data.get('relationship'),
            emergency_address = self.cleaned_data.get('emergency_address'),
            emergency_number = self.cleaned_data.get('emergency_number'),
            file = self.cleaned_data.get('file'),
            student_certificate_waec_image = self.cleaned_data.get(
                'student_certificate_waec_image '),
            student_certificate_jamb_image = self.cleaned_data.get(
                'student_certificate_jamb_image'),
            student_certificate_other_image = self.cleaned_data.get(
                'student_certificate_other_imag')

        )
        student.save()
        return user


class Userinterface_form(forms.ModelForm):
    class Meta:
        model = Userinterface_upload
        fields = ('picture', 'news_feed', 'event_feed', 'contact_us')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['news_feed'].widget.attrs.update({'class': 'form-control'})
        self.fields['event_feed'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['contact_us'].widget.attrs.update(
            {'class': 'form-control'})


class Userinterface_update_form(UserChangeForm):
    class Meta:
        model = Userinterface_upload
        fields = ('picture','news_feed','event_feed','contact_us')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['news_feed'].widget.attrs.update({'class': 'form-control'})
        self.fields['event_feed'].widget.attrs.update({'class': 'form-control'})
        self.fields['contact_us'].widget.attrs.update({'class': 'form-control'})




