from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('profile/<int:user_pk>', views.user_profile, name='user_detail'),
    path('<int:doctor_pk>/appoint', views.doctor_appoints, name='doctor_appoints'),
    path('<int:doctor_pk>/appoint-<slug:new_day>', views.doctor_appoints_with_day, name='doctor_appoints_with_day'),
    path('<int:doctor_pk>/appoint/<int:appoint_pk>', views.appoint_detail, name='appoint_detail'),
    path('<int:doctor_pk>/appoint/<int:appoint_pk>/make', views.make_appoint, name='make_appoint'),
    path('dashboard', views.moderator_dashboard, name='moderator_dashboard'),
    path('dashboard/appoint-create', views.create_appoint_moderator, name='create_appoint_moderator'),
    path('dashboard/<int:doctor_pk>', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/<int:doctor_pk>/appoint-create', views.create_appoint_doctor, name='create_appoint_doctor'),

]