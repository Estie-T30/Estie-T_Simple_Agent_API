from django.contrib import admin
from .models import House, HouseImage, Appointment, User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_agent', 'is_tenant', 'is_owner')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_agent', 'is_tenant', 'is_owner')

class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 1

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price', 'is_available', 'created_at')
    search_fields = ('title', 'address', 'description')
    list_filter = ('is_available', 'bedrooms', 'bathrooms', 'furnished', 'has_parking', 'pet_friendly')
    inlines = [HouseImageInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HouseImage)
class HouseImageAdmin(admin.ModelAdmin):
    list_display = ('house', 'caption')
    search_fields = ('caption',)
    # readonly_fields = ('house',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('house', 'tenant', 'date', 'time', 'status', 'created_at')
    search_fields = ('house__title', 'tenant__username', 'date')
    list_filter = ('status', 'date', 'time')
    readonly_fields = ('created_at', 'updated_at')
