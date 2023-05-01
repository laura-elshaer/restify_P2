# from django.conf.urls import url
from django.urls import path, include
from .views import (
    PropertyApiView,
    ReservationApiView,
    PropertySearch,
    ReservationsSearch,
    cancelRes,
    approveRes,
    approveCancel,
    deleteRes,
)

urlpatterns = [


    #properties
    path('property/', PropertyApiView.as_view()),
    path('property/<int:prop_id>/', PropertyApiView.as_view()), #put. get and delete call for properties
    path('property/search/', PropertySearch().as_view()), # searching for filtered results


    #reservations
    path('reservations/<', ReservationApiView.as_view()),
    path('reservations/<int:prop_id>/', ReservationApiView.as_view()),
    path('reservations/search/', ReservationsSearch.as_view()),
    path('reservations/cancel/<int:res_id>/', cancelRes),
    path('reservations/decision/<int:res_id>/<int:status>/', approveRes),
    path('reservations/cancel/pending/<int:res_id>/<int:status>/', approveCancel),
    path('reservations/delete/<int:res_id>', deleteRes),


]