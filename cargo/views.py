from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Cargo, CargoType
from .serializers import CargoSerializer,CargoTypeSerializer

class CargoListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CargoSerializer
    lookup_field = 'uuid'  # Use 'uuid' field for lookup

    def get_queryset(self):
        return Cargo.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender_name=self.request.user)

    def post(self, request, format=None):
        cargo_type_ids = request.data.pop('cargo_type', [])  # Remove cargo_type from request data
        serializer = CargoSerializer(data=request.data)
        if serializer.is_valid():
            cargo = serializer.save()

            # Associate cargo_type IDs with the created Cargo instance
            cargo.cargo_type.set(cargo_type_ids)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CargoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'uuid'  # Use 'uuid' field for lookup

class CargoCartegoriesCreateAPIView(generics.ListCreateAPIView):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    lookup_field = 'slug'  # Use 'uuid' field for lookup


class CargoByCategoryAPIView(generics.ListAPIView):
    serializer_class = CargoSerializer

    def list(self, request, *args, **kwargs):
        queryset = Cargo.objects.all()

        # Create a dictionary to store cargos grouped by category
        cargo_by_category = {}

        # Fetch all cargo types
        cargo_types = CargoType.objects.all()

        # Loop through each cargo type
        for cargo_type in cargo_types:
            # Fetch cargos belonging to the current cargo type
            cargos = queryset.filter(cargo_type=cargo_type)

            # Serialize the cargos
            cargo_serializer = self.get_serializer(cargos, many=True)

            # Store the cargos in the dictionary with the cargo type name as key
            cargo_by_category[cargo_type.name] = cargo_serializer.data

        return Response(cargo_by_category)
