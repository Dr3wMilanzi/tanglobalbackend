# views.py
from rest_framework import viewsets
from .models import VehicleType, Vehicle, Driver, Trip, VehicleImage
from .serializers import VehicleTypeSerializer, VehicleSerializer, DriverSerializer, TripSerializer, VehicleImageSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        vehicle = serializer.save(created_by=self.request.user)
        for image in self.request.FILES.getlist('images'):
            VehicleImage.objects.create(vehicle=vehicle, image=image)

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
