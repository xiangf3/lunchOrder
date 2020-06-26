from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('submit/', views.submit, name='submit'),
    path('done/', views.done, name='done'),
    path('records/', views.records, name='records'),
    path('failure/<slug:code>/', views.failure, name='failure'),
    path('edit/', views.edit, name='edit'),
]