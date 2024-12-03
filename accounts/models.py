from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone

from django.db.models import Q
from PIL import Image

from course.models import Program
from .validators import ASCIIUsernameValidator

# LEVEL_COURSE = "Level course"
DAYCEAR = "Daycear"
PRIMARY = "Primary"
JUNIOR_SECONDARY = "Junior Secondary"
SENIOR_SECONDARY = "Senior Secondary"


LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (DAYCEAR, "Daycear"),
    (PRIMARY, "Primary"),
    (JUNIOR_SECONDARY, "Junior Secondary"),
    (SENIOR_SECONDARY, "Senior Secondary"),

)
FATHER = "Father"
MOTHER = "Mother"
BROTHER = "Brother"
SISTER = "Sister"
GRAND_MOTHER = "Grand mother"
GRAND_FATHER = "Grand father"
OTHER = "Other"

RELATION_SHIP = (
    (FATHER, "Father"),
    (MOTHER, "Mother"),
    (BROTHER, "Brother"),
    (SISTER, "Sister"),
    (GRAND_MOTHER, "Grand mother"),
    (GRAND_FATHER, "Grand father"),
    (OTHER, "Other"),
)


class UserManager(UserManager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) |
                         Q(first_name__icontains=query) |
                         Q(last_name__icontains=query) |
                         Q(email__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class Userinterface_upload(models.Model):
    picture = models.ImageField(upload_to='images', null=True)
    news_feed = models.CharField(max_length=200)
    event_feed = models.CharField(max_length=200)
    contact_us = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.news_feed},{self.picture},{self.contact_us},{self.event_feed}'


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_dep_head = models.BooleanField(default=False)
    gender = models.CharField(max_length=50, choices=(("Male","Male"), ("Female","Female")), default="Male")
    switch = models.CharField(max_length=50, choices=(("True","True"), ("False","False")), default="False")
    dob = models.DateField(max,default='2000-01-01')
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(
        upload_to='profile_pictures/%y/%m/%d/', default='default.png', null=True)
    email = models.EmailField(blank=True, null=True)

    username_validator = ASCIIUsernameValidator()

    objects = UserManager()

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            return "Admin"
        elif self.is_student:
            return "Student"
        elif self.is_lecturer:
            return "Lecturer"
        elif self.is_parent:
            return "Parent"
        elif self.is_staff:
            return "staf"
        elif self.is_dep_head:
            return "HOD"

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + 'default.png'
            return no_picture

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(level__icontains=query) |
                         Q(department__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    # code = models.CharField(max_length=20, unique=True, blank=True)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    switch = models.CharField(max_length=50, choices=(("True","True"), ("False","False")), default="False")
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)

    objects = StudentManager()

    def __str__(self):
        return self.student.get_full_name
    class Meta:
        verbose_name_plural = "List of Students"

    # def __str__(self):
    #     return str(f"{self.code} - {self.first_name}{' '+self.middle_name if not self.middle_name == '' else ''} {self.last_name}")

#     def name(self):
#         return str(f"{self.first_name}{' '+self.middle_name if not self.middle_name == '' else ''} {self.last_name}")

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.code})
    
    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)


class UploadDocument(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='Student_files/', validators=[FileExtensionValidator(
        ['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    updated_date = models.DateTimeField(
        auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class ApplyingStudentManager(UserManager):
      def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) |
                         Q(first_name__icontains=query) |
                         Q(last_name__icontains=query) |
                         Q(email__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs




class ApplyingStudent(models.Model):
    username = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(max_length=30)
    LG_origin = models.CharField(max_length=30)
    state_origin = models.CharField(max_length=30)
    parent_name = models.CharField(max_length=30)
    parent_adress = models.CharField(max_length=30)
    Parent_number = models.CharField(max_length=30)
    Emergency_contact = models.CharField(max_length=30)
    relationship = models.CharField(max_length=30)
    emergency_address = models.CharField(max_length=30,)
    emergency_number = models.CharField(max_length=30)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    department = models.ForeignKey(
        Program, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='Student_files/', validators=[FileExtensionValidator(
        ['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    updated_date = models.DateTimeField(
        auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True)
    student_certificate_waec_image = models.ImageField(
        upload_to='student_certificate_img', default='default.png', null=True)
    student_certificate_jamb_image = models.ImageField(
        upload_to='student_certificate_img', default='default.png', null=True)
    student_certificate_other_image = models.ImageField(
        upload_to='student_certificate_img', default='default.png', null=True)
    
    objects = ApplyingStudentManager()
    def __str__(self):
        return str(self.file)

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'


    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.username.delete()
        super().delete(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    # id_number = models.CharField(max_length=20, unique=True, blank=True)



class Parent(models.Model):
    """
    Connect student with their parent, parents can 
    only view their connected students information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(
        Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # What is the relationship between the student and the parent (i.e. father, mother, brother, sister)
    relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)

    def __str__(self):
        return  "{}".format(self.user.username, self.student, self.last_name,self.first_name,self.phone,self.email,self.relation_ship) 


class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Program, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.user)


class StudentApplication(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    date_of_birth = models.DateField(max_length=30)
    LG_origin = models.CharField(max_length=30)
    state_origin = models.CharField(max_length=30)
    parent_name = models.CharField(max_length=30)
    parent_adress = models.CharField(max_length=30)
    parent_number = models.CharField(max_length=30)
    emergency_contact = models.CharField(max_length=30)
    relationship = models.CharField(max_length=30)
    emergency_address = models.CharField(max_length=30)
    emergency_number = models.CharField(max_length=30)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    department = models.ForeignKey(
        Program, on_delete=models.CASCADE, null=True)
    student_files = models.FileField(upload_to='Student_files/', validators=[FileExtensionValidator(
        ['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    student_certificate_waec_image = models.ImageField(
        upload_to='student_certificate_img', default='default.png', null=True)
    student_certificate_jamb_image = models.ImageField(
        upload_to='student_certificate_img', default='default.png', null=True)
    student_certificate_other_image = models.ImageField(
        upload_to='student_certificate_img', default='default.png', null=True)
    student_passport = models.ImageField(
        upload_to='student_passport', default='default.png', null=True)
    def __str__(self):
            return str(self.student_files)[6:]

    def get_extension_short(self):
        ext = str(self.student_files).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'

    def delete(self, *args, **kwargs):
        self.student_files.delete()
        super().delete(*args, **kwargs)

