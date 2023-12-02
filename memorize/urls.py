from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('calendar/', views.calendar_view),
    path('ping/', views.PingView),
    path('admin/', admin.site.urls),
]
