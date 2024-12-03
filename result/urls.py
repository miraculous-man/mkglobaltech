from django.urls import path
from . import views
from .views import (
    add_score, add_score_for, grade_result, assessment_result, result_sheet,child_result,
    course_registration_form, result_sheet_pdf_view, student_addmission_letter, result_template
)


urlpatterns = [
    path('manage-score/', add_score, name='add_score'),
    path('manage-score/<int:id>/', add_score_for, name='add_score_for'),
    
    path('grade/', grade_result, name="grade_results"),
    path('assessment/', assessment_result, name="ass_results"),
    
    path('result_template/', result_template, name='result_template'),
    path('result_sheet/', result_sheet, name='result_sheet'),
    path('childs_result/', child_result, name='child_result'),

    path('views_index/', views.index, name='view_index'),
    path('result_pdf/', views.Viewpdf.as_view(), name='pdf_view'),
    path('pdf_download/', views.Downloadpdf.as_view(), name='pdf_downlaod'),


	path('result/print/<int:id>/', result_sheet_pdf_view, name='result_sheet_pdf_view'),
	path('registration/form/', course_registration_form, name='course_registration_form'),
   	path('admission_letter/<int:pk>', student_addmission_letter,name='addmission_letter'),

]
