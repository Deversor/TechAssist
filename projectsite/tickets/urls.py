# tickets/urls.py

from django.urls import path
from .views import HomePageView, TicketListView, TicketCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/create/', TicketCreateView.as_view(), name='ticket-create'),
]