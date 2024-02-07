from django.contrib import admin
from django.urls import path
from . import views
from .views import UpdateResView, DeleteResView
#from .views import PostListView
                    



urlpatterns = [
    path('', views.home , name='reservation-home'),
    #path('', PostListView.as_view() , name = 'reservation-home'),
    path('reservation/', views.reservation, name='reservation-reservation'),
    path('reservation_details/<int:post_id>/', views.reservationDetails, name='reservation-details'),
    path('reservation_update/<int:pk>/', UpdateResView.as_view(), name='reservation-update'),
    path('reservation_delete/<int:pk>/', DeleteResView.as_view(), name='reservation-delete')
]



