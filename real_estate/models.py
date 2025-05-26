from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_image

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', validators=[validate_image], blank=True, null=True)
    is_agent = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} - {self.email}'

class House(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses')
    title = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_footage = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    has_parking = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    is_verified_by_agent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.owner.username}"

class HouseImage(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='house_images/', validators=[validate_image])
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.house.title} - {self.caption}"

TIME_CHOICES = [
    ('9AM', '9AM'),
    ('10AM', '10AM'),
    ('11AM', '11AM'),
    ('12PM', '12PM'),
    ('1PM', '1PM'),
    ('2PM', '2PM'),
    ('3PM', '3PM'),
    ('4PM', '4PM'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
]

class Appointment(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='appointments')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.CharField(choices=TIME_CHOICES, max_length=5)
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant.username} - {self.house.title} - {self.date} {self.time}"


