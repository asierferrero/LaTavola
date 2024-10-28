from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('sarrera/', views.sarrera, name='login'),
    path('logout', views.logout_view)
]
