from django.urls import path

from . import views

app_name = 'checks'

urlpatterns = [
    path('add_new_order/', views.add_new_order),
]
