from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
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
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', _('Enter a valid phone number.'))]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name if self.first_name else self.email.split('@')[0]
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.pk})
    
    def save(self, *args, **kwargs):
        if self.profile_picture:
            fs = FileSystemStorage()
            filename = fs.save(self.profile_picture.name, self.profile_picture)
            self.profile_picture = fs.url(filename)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError(_('Date of birth cannot be in the future.'))
        if self.phone_number and not RegexValidator(r'^\+?1?\d{9,15}$')(self.phone_number):
            raise ValidationError(_('Enter a valid phone number.'))
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def get_profile_picture(self):
        if self.profile_picture:
            return File(self.profile_picture)
        return None
    
    def delete_profile_picture(self):
        if self.profile_picture:
            fs = FileSystemStorage()
            fs.delete(self.profile_picture.name)
            self.profile_picture = None
            self.save()
            
