from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yelpSearch/', views.yelpSearch, name='yelpSearch'),
    path('restroom/<int:r_id>', views.restroom, name='restroom'),
]
