from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['ip_address', 'created_at', 'updated_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'social_media_link')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'ip_address', 'created_at', 'updated_at')
        }),
    )

admin.site.register(Contact, ContactAdmin)
