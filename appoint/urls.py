from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('<int:doctor_pk>', views.doctor_profile, name='doctor_detail'),
    path('<int:doctor_pk>/upload-photo', views.upload_doctor_photo, name='doctor_upload_photo'),
    path('profile/<int:user_pk>', views.user_profile, name='user_detail'),
    path('<int:doctor_pk>/appoint', views.doctor_appoints, name='doctor_appoints'),
    path('<int:doctor_pk>/appoint-<slug:new_day>', views.doctor_appoints_with_day, name='doctor_appoints_with_day'),
    path('<int:doctor_pk>/appoint/<int:appoint_pk>', views.appoint_detail, name='appoint_detail'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/appoint-create', views.create_appoint, name='create_appoint'),
    path('dashboard/appoints-create', views.create_few_appoints, name='create_few_appoints'),

]