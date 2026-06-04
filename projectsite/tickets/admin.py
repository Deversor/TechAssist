from django.contrib import admin
# Import your specific models from models.py
from .models import Ticket  

# Register the Ticket model so it appears in Django Admin
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # This displays your data columns clearly in a table grid
    list_display = ('id', 'facility_vector', 'priority', 'current_status') 
    list_filter = ('current_status', 'priority')