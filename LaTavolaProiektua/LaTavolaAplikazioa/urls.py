from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('saskia/', views.saskia, name='saskia'),
    path('verify/<int:id>/', views.verify_view, name='verify'),
    path('api/produktuak/', views.Produktuak_APIView.as_view()),
    path('api/produktuak/<int:pk>/', views.Produktuak_APIView_Detail.as_view()),
    path('api/ContsumituT2/', views.T2Consume_API.as_view())
]
