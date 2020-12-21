from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:doctor_id>/appoints', views.doctor_appoints, name='doctor_appoints'),
    #path('<int:pk>', views.DoctorDetailView.as_view(), name='doctor_detail'),
    #path('<int:pk>/appoint/<int:pk>', views.AppointDetailView.as_view(), name='appoint_detail'),
]