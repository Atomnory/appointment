from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/appoints', views.DoctorAppointsView.as_view(), name='appoints'),
    #path('<int:pk>/detail', views.DoctorDetailView.as_view(), name='doctor_detail'),
    #path('<int:pk>/appoint/<int:pk>', views.AppointDetailView.as_view(), name='appoint_detail'),
]