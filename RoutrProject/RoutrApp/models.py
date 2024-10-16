from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.email


class DriverTripRecord(models.Model):
    date = models.DateField()
    company_address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255)
    manifest = models.CharField(max_length=255, blank=True, null=True)
    truck_no = models.CharField(max_length=255, blank=True, null=True)
    trailer_no = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    starting_mileage = models.DecimalField(max_digits=10, decimal_places=2)
    ending_mileage = models.DecimalField(max_digits=10, decimal_places=2)
    starting_location = models.CharField(max_length=255)
    ending_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.driver_name} - {self.company_name} - Start: {self.starting_location} - End: {self.ending_location}"


class Stop(models.Model):
    trip_record = models.ForeignKey(DriverTripRecord, on_delete=models.CASCADE, related_name='stops')
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_address = models.CharField(max_length=255, blank=True, null=True)
    pallets_in = models.IntegerField(blank=True, null=True)
    pallets_out = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stop for {self.trip_record} - {self.customer_name}"


class FuelPurchaseRecord(models.Model):
    state = models.CharField(max_length=100)
    date = models.DateField()
    invoice_number = models.CharField(max_length=100)
    gallons = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    dollar_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fuel_stop_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    trip_record = models.OneToOneField('DriverTripRecord', on_delete=models.CASCADE, related_name='fuel_purchase', null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.invoice_number}"
