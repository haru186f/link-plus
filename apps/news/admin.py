from django.contrib import admin
from .models import ReceivedEmail

@admin.register(ReceivedEmail)
class ReceivedEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'received_at', 'is_read')
    search_fields = ('subject', 'sender', 'body')