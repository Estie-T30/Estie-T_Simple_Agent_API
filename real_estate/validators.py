from django.core.exceptions import ValidationError


def validate_image(image):
    """
    Validate the uploaded image.
    """
    file_size = image.size
    megabyte_limit = 3   # MB
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Image file size exceeds the limit of {megabyte_limit} MB.')
    if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('Image file must be a PNG, JPG, or JPEG.')
    
def validate_appointment_overlap(house, date, time, appointment_id=None):
    from .models import Appointment
    
    overlaping = Appointment.objects.filter(
        house=house,
        date=date,
        time=time
    )
    if appointment_id:
        overlaping = overlaping.exclude(pk=appointment_id)
    
    if overlaping.exists():
        raise ValidationError('An appointment for this house at the selected date and time already exists.')
    
    
