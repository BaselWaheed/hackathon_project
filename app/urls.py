from django.urls import path
from app import views


urlpatterns = [

    path('reels/',views.Homepage.as_view(), name = 'homepage'),

    path('likes/', views.AddOrDeleteLikeView.as_view() , name = 'likes') ,

    path('comment/' , views.CommentAPI.as_view() , name = 'comment'),

    path('decrypt/' , views.DecryptAPI.as_view() , name='decrypt') ,
    
]