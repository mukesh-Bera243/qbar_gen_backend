from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserDetails, PaymentDetail, QBarDetails

@admin.register(UserDetails)
class UserDetailsAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'mobilenumber', 'is_staff', 'is_superuser']
    search_fields = ['email', 'mobilenumber']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('mobilenumber',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'amount', 'currency', 'subscription_type',
        'transaction_id', 'payment_date', 'status',
        'created_at', 'updated_at'
    )
    list_filter = ('status', 'currency', 'subscription_type')
    search_fields = ('user__email', 'transaction_id')

@admin.register(QBarDetails)
class QBarDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'is_login',
        'qrcode_download_count', 'barcode_download_count', 'view_count',
        'ip_address', 'location_info',
        'latest_created_at', 'latest_updated_at'
    )
    list_filter = ('user__email', 'is_login')
    search_fields = ('user__email', 'ip_address', 'location_info')
