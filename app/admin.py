from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Session, Semester, NewsAndEvents, Contact_us_info

class Contact_us_infoAdmin(admin.ModelAdmin):
    list_display = [  'name','email','subject','description']
   

admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(NewsAndEvents)
admin.site.register(Contact_us_info)
