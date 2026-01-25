from django.contrib import admin
from .models import Payment, Order, OrderProduct, PersonalInfo
from django.utils.html import format_html
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'payment_method_display', 'payment_status_display', 'order_total', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered', 'payment__payment_method', 'payment__status']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    list_editable = ['status']
    inlines = [OrderProductInline]

    def payment_method_display(self, obj):
        if obj.payment:
            if obj.payment.payment_method == 'DIRECT':
                return format_html('<span style="color: #007bff;">💰 Direct</span>')
            elif obj.payment.payment_method == 'CRYPTO':
                return format_html('<span style="color: #28a745;">₿ Crypto</span>')
            return obj.payment.get_payment_method_display()
        return '-'
    payment_method_display.short_description = 'Payment Method'

    def payment_status_display(self, obj):
        if obj.payment:
            if obj.payment.status == 'Completed':
                return format_html('<span style="color: #28a745; font-weight: bold;">✓ {}</span>', obj.payment.status)
            elif obj.payment.status == 'Pending':
                return format_html('<span style="color: #ffc107; font-weight: bold;">⏳ {}</span>', obj.payment.status)
            return obj.payment.status
        return '-'
    payment_status_display.short_description = 'Payment Status'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['workflow_info'] = {
            'title': 'Order Processing Workflow',
            'steps': [
                'Step 1: Verify payment in Payment admin (set Payment Status to "Completed")',
                'Step 2: Order status will auto-update to "Accepted" when payment is verified',
                'Step 3: Change Order Status to "Completed" when order is fulfilled',
                'Note: Changing Order Status to "Accepted" or "Completed" will auto-complete the payment'
            ]
        }
        return super().changelist_view(request, extra_context=extra_context)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at', 'view_proof']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['payment_id', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['payment_id', 'user', 'payment_method', 'amount_paid', 'crypto_wallet_url', 'payment_proof_image', 'created_at']
    list_per_page = 20
    list_editable = ['status']

    def view_proof(self, obj):
        if obj.crypto_payment_proof:
            return format_html('<a href="{}" target="_blank">View Proof</a>', obj.crypto_payment_proof.url)
        return '-'
    view_proof.short_description = 'Payment Proof'

    def payment_proof_image(self, obj):
        if obj.crypto_payment_proof:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;" />', obj.crypto_payment_proof.url)
        return 'No proof uploaded'
    payment_proof_image.short_description = 'Payment Proof Image'

    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'user', 'payment_method', 'amount_paid', 'created_at')
        }),
        ('Payment Verification', {
            'fields': ('status',),
            'description': '⚠️ IMPORTANT: When you change this to "Completed", the related order status will automatically update to "Accepted". Verify payment details before confirming.'
        }),
        ('Crypto Payment Details', {
            'fields': ('crypto_wallet_url', 'payment_proof_image'),
            'classes': ('collapse',),
            'description': 'View crypto wallet URL and payment proof screenshot for verification'
        }),
    )

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(PersonalInfo)   
