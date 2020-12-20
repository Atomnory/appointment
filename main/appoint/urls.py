from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/appoint', views.AppointView.as_view(), name='appoint'),
    #path('<int:pk>/detail', views.DoctorDetailView.as_view(), name='doctor_detail'),
    #path('<int:pk>/appoint/<int:pk>', views.AppointDetailView.as_view(), name='appoint_detail'),
]