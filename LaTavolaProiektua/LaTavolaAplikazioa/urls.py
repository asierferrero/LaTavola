from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    
    path('admin-home/', views.admin_home_view , name='admin_home'),
    
    path('admin-home/produktuak-list/', views.admin_produktuak_list , name='produktuak-list'),
    path('admin-home/produktuak-new/', views.produktua_new , name='produktuak-new'),
    path('admin-home/produktuak/delete/<int:id>/', views.produktuak_delete, name='produktuak-delete'),
    path('admin-home/produktuak/edit/<int:id>/', views.produktuak_edit, name='produktuak-edit'),
    
    path('admin-home/bezeroak-list/', views.admin_bezeroak_list , name='bezeroak-list'),
    path('admin-home/bezeroak/delete/<int:id>/', views.bezeroak_delete, name='bezeroak-delete'),
    path('admin-home/bezeroak/edit/<int:id>/', views.bezero_edit, name='bezero-edit'),
    
    path('admin-home/alergenoak-list/', views.admin_alergenoak_list, name='alergeno-list'),
    path('admin-home/alergenoak/delete/<int:id>/', views.alergenoak_delete, name='alergenoak-delete'),
    path('admin-home/alergenoak-new/', views.alergenoa_new , name='alergenoak-new'),
    path('admin-home/alergenoak/edit/<int:id>/', views.alergenoak_edit, name='alergenoak-edit'),
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('saskia/', views.saskia, name='saskia'),
    path('iritzia/', views.iritzia_sartu, name='iritzia_sartu'),
    
    path('verify/<int:id>/', views.verify_view, name='verify'),
    
    path('api/produktuak/', views.Produktuak_APIView.as_view()),
    path('api/produktuak/<int:pk>/', views.Produktuak_APIView_Detail.as_view()),
    path('api/contsumituT2/', views.T2Consume_API.as_view())
]
