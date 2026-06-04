from django.urls import path
from .views import (
    HomePageView, 
    TicketListView, 
    TicketCreateView, 
    TicketUpdateView, 
    TicketDeleteView
)
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/raise/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]