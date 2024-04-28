from rest_framework import generics
from .models import Cargo
from .serializers import CargoSerializer

class CargoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'uuid'  # Use 'uuid' field for lookup

class CargoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'uuid'  # Use 'uuid' field for lookup
