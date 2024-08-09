# views.py
from rest_framework import viewsets
from rest_framework.decorators import action  # Add this import
from rest_framework.response import Response
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
    
    @action(detail=False, methods=['get'], url_path='my-vehicles', permission_classes=[IsAuthenticated])
    def get_vehicles_for_user(self, request):
        """
        Custom action to get vehicles owned by the logged-in user.
        """
        user = request.user
        vehicles = Vehicle.objects.filter(created_by=user)
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)
    
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
