# tickets/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket

class HomePageView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'home.html'
    context_object_name = 'dashboard_tickets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Superusers can see everything globally
        if user.is_superuser:
            base_qs = Ticket.objects.all()
        # Fall back to standard user role constraints
        elif hasattr(user, 'profile') and user.profile.role == 'USER':
            base_qs = Ticket.objects.filter(created_by=user)
        elif hasattr(user, 'profile') and user.profile.role == 'TECHNICIAN':
            base_qs = Ticket.objects.filter(assigned_to=user)
        else:
            base_qs = Ticket.objects.all()

        # Compute key analytics metrics
        context['open_tickets'] = base_qs.filter(status='OPEN').count()
        context['resolved_tickets'] = base_qs.filter(status='RESOLVED').count()
        context['pending_tickets'] = base_qs.filter(status='PENDING').count()
        context['high_priority_tickets'] = base_qs.filter(priority__in=['HIGH', 'URGENT']).count()
        
        # Send tickets to the table preview for administrators and fallback roles
        if user.is_superuser:
            context['dashboard_tickets'] = Ticket.objects.all().order_by('-created_at')[:10]
        else:
            context['dashboard_tickets'] = base_qs.order_by('-created_at')[:5]
            
        return context

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        
        # Role-based visibility logic
        if hasattr(user, 'profile') and user.profile.role == 'USER':
            qs = Ticket.objects.filter(created_by=user)
        elif hasattr(user, 'profile') and user.profile.role == 'TECHNICIAN':
            qs = Ticket.objects.filter(assigned_to=user)
        else:
            qs = Ticket.objects.all()

        # Complex query text search parsing across domain boundaries
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(room_number__icontains=query)
            )
            
        # Global multi-parameter column sort sorting engine execution
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
        # QR Engine Auto-Fill Parameter Hook
        initial['building'] = self.request.GET.get('building', '')
        initial['room_number'] = self.request.GET.get('room', '')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Alerts frontend if request stems from a scanned QR configuration
        context['is_qr'] = 'building' in self.request.GET or 'room' in self.request.GET
        return context

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    # Technicians and admins can edit extra control parameters like status and assignment tracking
    fields = ['title', 'category', 'description', 'building', 'room_number', 'priority', 'status', 'assigned_to']
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')