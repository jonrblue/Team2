from django.urls import path

from . import views
app_name ="naturescall"
urlpatterns = [
    path('', views.index, name='index'),
    path('yelpSearch/', views.yelpSearch, name='yelpSearch'),
    path('addR/<slug:r_id>', views.addR, name ='addR'),
]
