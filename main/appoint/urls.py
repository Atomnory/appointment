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

]