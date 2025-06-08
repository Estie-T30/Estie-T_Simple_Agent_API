from django.shortcuts import get_object_or_404
from .models import House, Appointment, User
from .serializers import HouseListSerializer, UserSerializers, HouseImageSerializer, HouseCreateSerializer, PublicHouseListSerializer, HouseDetailSerializer, AppointmentSerializer
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrAgent, IsAppointmentOwner, IsOwnerOnly, IsTenantUser



# Create your views here.
class UserListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        paginator = PageNumberPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializers(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserCreateView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'User creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AllHouseListView(APIView):
     permission_classes = [IsAdminOrAgent]

     def get(self, request):
        houses = House.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_houses = paginator.paginate_queryset(houses, request)
        serializer = HouseListSerializer(paginated_houses, many=True)
        return paginator.get_paginated_response(serializer.data)

class PublicHouseListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        houses = House.objects.filter(is_available=True, is_verified_by_agent=True).select_related('owner').prefetch_related('images')
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_houses = paginator.paginate_queryset(houses, request)
        serializer = PublicHouseListSerializer(paginated_houses, many=True)
        return paginator.get_paginated_response(serializer.data)

class PublicHouseDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        house = get_object_or_404(House, pk=pk, is_available=True)
        serializer = PublicHouseListSerializer(house)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
class HouseCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request):
        serializer = HouseCreateSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'detail': 'House created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'House creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HouseImageCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        house_id = request.data.get('house_id')
        if not house_id:
             return Response({'detail': 'House_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        house = get_object_or_404(House, pk=house_id)

        if request.user != house.owner and not request.user.is_staff:
             return Response({'detail': 'Not authorized to add images to this house.'}, status=status.HTTP_403_FORBIDDEN)
        
        images = request.FILES.getlist('images') # Expecting a list of images
        captions = request.data.getlist('captions') # List of captions

        if not images:
             return Response({'detail': 'At least one image is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        if len(images) != len(captions):
             return Response({'detail': 'Number of captions must match number of images'}, status=status.HTTP_400_BAD_REQUEST)
        
        created_images = []
        errors = []

        for i, image in enumerate(images):
            caption = captions[i] if i < len(captions) else None
            data = {'image': image, 'caption': caption}
            serializer = HouseImageSerializer(data=data)
            if serializer.is_valid():
                serializer.save(house=house)
                created_images.append(serializer.data)
            else: 
                errors.append(serializer.errors)

        if errors:
            return Response({'detail': 'Some Images upload failed', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Images uploaded successfully', 'data': created_images}, status=status.HTTP_201_CREATED)


class HouseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def put(self, request, pk):
            house = get_object_or_404(House, pk=pk)
            self.check_object_permissions(request, house)  # Check if the user has permission to edit this house
            if request.user != house.owner and not request.user.is_staff:
                return Response({'detail': 'Not authorized to edit this house.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = HouseDetailSerializer(house, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'House updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'detail': 'House update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
            house = get_object_or_404(House, pk=pk)
            self.check_object_permissions(request, house)  # Check if the user has permission to delete this house
            if request.user != house.owner and not request.user.is_staff:
                return Response({'detail': 'Not authorized to delete this house.'}, status=status.HTTP_403_FORBIDDEN)
            house.delete()
            return Response({'detail': 'House deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class AppointmentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_tenant:
              appointments = Appointment.objects.filter(tenant=user)
        elif user.is_owner or user.is_staff:
                appointments = Appointment.objects.all()
        else:
             appointments = Appointment.objects.none()  # No appointments for other users

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_appointments = paginator.paginate_queryset(appointments, request)
        serializer = AppointmentSerializer(paginated_appointments, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.user)
            return Response({'detail': 'Appointment Creation Successful', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Appointment Creation Failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAppointmentOwner]

    def get(self, request, pk):
            appointment = get_object_or_404(Appointment, pk=pk)
            serializer = AppointmentSerializer(appointment)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
    def put(self, request, pk):
            appointment = get_object_or_404(Appointment, pk=pk)
            serializer = AppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Appointment updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'detail': 'Appointment update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
            appointment = get_object_or_404(Appointment, pk=pk)
            appointment.delete()
            return Response({'detail': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
class AppointmentReadOnlyView(APIView):
    permission_classes = [IsAdminOrAgent]

    def get(self, request, pk):
            appointment = get_object_or_404(Appointment, pk=pk)
            serializer = AppointmentSerializer(appointment)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)