from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:doctor_id>/appoints', views.doctor_appoints, name='doctor_appoints'),
    #path('<int:pk>', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('<int:doctor_id>/appoint/<int:appoint_id>', views.appoint_detail, name='appoint_detail'),
]