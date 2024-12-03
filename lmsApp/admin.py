from django.contrib import admin
from lmsApp import models

# Register your models here.
# admin.site.register(models.Groups)

class CategoryAdmin(admin.ModelAdmin):
    list_display = [  'name','description','status','delete_flag',
        'date_added', 'date_created']
   

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [  'name','description','status','delete_flag',
        'date_added', 'date_created']



class BooksAdmin(admin.ModelAdmin):
    list_display = [  'sub_category','isbn','title','description','author',
        'date_added', 'date_created']

admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.Books,BooksAdmin)

# admin.site.unregister(Group)
