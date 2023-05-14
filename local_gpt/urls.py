from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('ping/', views.PingView),
    path('admin/', admin.site.urls),
]
