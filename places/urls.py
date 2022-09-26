from django.urls import path
from . import views



app_name = 'places'

urlpatterns = [

    path('search/', views.SearchAPI.as_view() , name = 'search'),

    path("profile/" , views.UserDetailsAPI.as_view() , name= 'prodile') ,

    path('all/', views.PlacesAPI.as_view() , name= 'PlacesAPI'),

    
]
