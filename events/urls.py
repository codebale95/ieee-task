from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events_list, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('purchase_ticket/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),
]
