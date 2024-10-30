from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<int:id>/<str:username>/', views.verify_view, name='verify'),
]
