from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    
    path('admin-home/', views.admin_home_view , name='admin_home'),
    path('admin-home/bezeroak-list/', views.admin_bezeroak_list , name='bezeroak-list'),
    path('admin-home/produktuak-list/', views.admin_produktuak_list , name='produktuak-list'),
    path('admin-home/produktuak-new/', views.produktua_new , name='produktuak-new'),
    path('produktuak/delete/<int:id>/', views.produktuak_delete, name='produktuak-delete'),
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<int:id>/<str:username>/', views.verify_view, name='verify'),
]
