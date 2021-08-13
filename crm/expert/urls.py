from django.urls import path
from . import views

app_name = 'expert'
urlpatterns = [
    path('login', views.ExpertLoginView.as_view(), name='login')
]
