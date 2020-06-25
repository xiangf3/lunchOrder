from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('submit/', views.submit, name='submit'),
    path('done/', views.done, name='done'),
    path('failure/<int:code>/', views.failure, name='failure'),
]