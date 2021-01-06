from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:doctor_id>/appoint', views.doctor_appoints, name='doctor_appoints'),
    path('<int:doctor_id>/appoint-<slug:new_day>', views.doctor_appoints_with_day, name='doctor_appoints_with_day'),
    path('<int:doctor_id>/appoint/<int:appoint_id>', views.appoint_detail, name='appoint_detail'),
    path('<int:doctor_id>/appoint/<int:appoint_id>/make', views.make_appoint, name='make_appoint'),
    #path('<int:pk>', views.DoctorDetailView.as_view(), name='doctor_detail'),
]