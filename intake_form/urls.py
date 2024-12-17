from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_process_form, name='submit_process_form'),
    path('success/', views.success_page, name='success_page'),
]