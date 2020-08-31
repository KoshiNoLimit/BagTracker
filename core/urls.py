from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('home/', views.Home.as_view(), name='home'),
    path('<int:pk>/', views.DeskView.as_view(), name='desk'),
    path('<int:dpk>/<int:tpk>', views.TaskView.as_view(), name='task'),
]
