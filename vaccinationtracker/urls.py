

from django.urls import path
from .views import (login_view, dashboard, logout_view, student_details_page, save_student_details,
 genearte_report, FilterReport, create_vaccine_form, create_vaccination_details, update_vaccination_drive, update, updaterecord, downlaod_as_csv)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('student_detail/', student_details_page, name='student_detail'),
    path('create_vaccination_details/', create_vaccination_details, name='create_vaccination_details'),
    path('save_student_detail/', save_student_details, name='save_student_detail'),
    path('genearte_report/', genearte_report, name='genearte_report'),
    path('downlaod_as_csv/', downlaod_as_csv, name='downlaod_as_csv'),
    path('filter_report/', FilterReport.as_view(), name='filter_report'),
    path('create_vaccine_form/', create_vaccine_form, name='create_vaccine_form'),
    path('create_vaccine_form/', create_vaccine_form, name='create_vaccine_form'),
    path('update_vaccination_drive/', update_vaccination_drive, name='update_vaccination_drive'),
    path('dashboard/update/<int:id>', update, name='update'),
    path('dashboard/update/updaterecord/<int:id>', updaterecord, name='updaterecord'),

]
