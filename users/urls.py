from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),


    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name="user_profiles"),
    
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),

    path('create_skill/', views.createSkill, name="create_skill"),
    path('update_skill/<str:pk>/', views.updateSkill, name="update_skill"),
    path('delete_skill/<str:pk>/', views.deleteSkill, name="delete_skill"),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),


]