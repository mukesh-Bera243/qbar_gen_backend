from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserDetailsManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

class UserDetails(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    mobilenumber = models.CharField(max_length=12, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)

    objects = UserDetailsManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Username is not required

    def __str__(self):
        return self.email

class PaymentDetail(models.Model):
    user = models.ForeignKey(
        UserDetails,
        related_name='payments',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')  # e.g., 'USD', 'INR'
    subscription_type = models.CharField(max_length=50)       # e.g., 'monthly', 'annual'
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    financial_year = models.CharField(max_length=20,null=True,blank=True)
    month = models.CharField(max_length=20,null=True,blank=True)   
    current_year = models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        return f"{self.user.email} - {self.transaction_id}"

class QBarDetails(models.Model):
    user = models.ForeignKey(
        'UserDetails',  # string if class is below or in another file
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='qbars'
    )
    is_login = models.BooleanField(default=False)

    # Tracking fields
    qrcode_download_count = models.PositiveIntegerField(default=0)
    barcode_download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)  # Total times accessed/viewed

    # Optional: Details about traffic
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    location_info = models.CharField(max_length=255, null=True, blank=True)  # e.g., city/country if resolved via IP
    latest_created_at = models.DateTimeField(default=timezone.now)
    latest_updated_at = models.DateTimeField(null=True, blank=True)
    financial_year = models.CharField(max_length=20,null=True,blank=True)
    month = models.CharField(max_length=20,null=True,blank=True)   
    current_year = models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        return f"{self.user.email if self.user else 'Anonymous'}"
