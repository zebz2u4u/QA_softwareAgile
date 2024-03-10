from django.urls import path

from . import views
urlpatterns = [
    path('', views.homePage, name=""),

    path('register', views.register, name="register"),
    
    path('login', views.login, name="login"),

    path('logout', views.logout, name="logout"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('create-record', views.createRecord, name="create-record"),

    path('update-request/<int:pk>/', views.updateRecord, name='update-record'),
]