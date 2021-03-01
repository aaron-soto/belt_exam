from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('process_trip', views.process_trip),
    path('process_login', views.process_login),
    path('process_logout', views.process_logout),
    path('process_register', views.process_register),
    path('update_trip/<int:num>', views.update_trip),
    path('trips/new', views.trips_new),
    path('trips/<int:num>', views.trip_page),
    path('trips/<int:num>/join', views.trip_join),
    path('trips/<int:num>/edit', views.trip_update_page),
    path('trips/<int:num>/remove', views.trip_remove),
    path('trips/<int:num>/cancel', views.trip_cancel),
]
