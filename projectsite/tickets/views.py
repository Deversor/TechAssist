# tickets/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket

class HomePageView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'home.html'
    context_object_name = 'tickets'  # Matches standard ListView iteration hooks

    def get_context_data(self, **kwargs):
        # 1. Grab default list context architecture map
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 2. Apply strict role visibility filter parameters
        if hasattr(user, 'profile') and user.profile.role == 'USER':
            base_qs = Ticket.objects.filter(created_by=user)
        elif hasattr(user, 'profile') and user.profile.role == 'TECHNICIAN':
            base_qs = Ticket.objects.filter(assigned_to=user)
        else:
            # Fallback configuration: Admin users see every entry globally
            base_qs = Ticket.objects.all()

        # 3. Compute analytics health metrics using precise variable signatures
        context['open_tickets'] = base_qs.filter(status='OPEN').count()
        context['resolved_tickets'] = base_qs.filter(status='RESOLVED').count()
        context['pending_tickets'] = base_qs.filter(status='PENDING').count()
        context['high_priority_tickets'] = base_qs.filter(priority__in=['HIGH', 'URGENT']).count()
        
        # 4. Explicitly bind the filtered worklist array for the home summary table
        context['dashboard_tickets'] = base_qs.order_by('-created_at')[:5]
        return context

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'USER':
            qs = Ticket.objects.filter(created_by=user)
        elif hasattr(user, 'profile') and user.profile.role == 'TECHNICIAN':
            qs = Ticket.objects.filter(assigned_to=user)
        else:
            qs = Ticket.objects.all()

        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(room_number__icontains=query)
            )
            
        sort_by = self.request.GET.get('sort_by', '-created_at')
        return qs.order_by(sort_by)

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'category', 'description', 'building', 'room_number', 'priority']
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['building'] = self.request.GET.get('building', '')
        initial['room_number'] = self.request.GET.get('room', '')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_qr'] = 'building' in self.request.GET or 'room' in self.request.GET
        return context

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['title', 'category', 'description', 'building', 'room_number', 'priority', 'status', 'assigned_to']
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')