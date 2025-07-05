from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),  
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('', views.post_list, name='post_list'),

    path('parametre.html', views.profile_settings, name='profile_settings'), 
     path('profile/', views.profile_view, name='profile'),

]
