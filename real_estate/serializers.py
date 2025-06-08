from .models import User, House, HouseImage, Appointment
from rest_framework import serializers
from .validators import validate_appointment_overlap

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', 'house', 'image', 'caption']
        read_only_fields = ['id', 'house']

class PublicHouseListSerializer(serializers.ModelSerializer):
    images = HouseImageSerializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = ['id', 'title', 'address', 'price', 'bedrooms', 'bathrooms', 'is_available', 'pet_friendly', 'has_parking', 'furnished', 'images']
        read_only_fields = ['id']

class HouseListSerializer(serializers.ModelSerializer):
    images = HouseImageSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = House
        fields = '__all__'
        read_only_fields = ['id', 'owner']

class HouseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
        read_only_fields = ['owner']

class HouseDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = House
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        house = data.get('house')
        date = data.get('date')
        time = data.get('time')
        appointment_id = self.instance.pk if self.instance else None

        validate_appointment_overlap(house, date, time, appointment_id)
        
        return data

    