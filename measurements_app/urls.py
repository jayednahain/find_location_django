from django.urls import path
from measurements_app import views


urlpatterns = [
    path('',views.distanceCalculationView,name = "distance_link")
]
