from django.urls import path

from . import views

app_name = 'checks'

urlpatterns = [
    path('add_new_order/', views.add_new_order, name='add_new_order'),
    path(
        'get_rendered_checks_at_point/<int:point>/',
        views.get_rendered_checks_at_point
    ),
]
