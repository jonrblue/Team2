from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yelpSearch/', views.yelpSearch, name='yelpSearch'),
    path('yelpSearch/restroom/<int:r_id>', views.show_details, name='restroom'),
]
