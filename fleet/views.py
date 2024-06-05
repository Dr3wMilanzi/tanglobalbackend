from rest_framework import viewsets,generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Vehicle,VehicleImage,VehicleType
from .serializers import VehicleSerializer,VehicleImageSerializer,VehicleTypeSerializer

class VehicleCreateList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        docs = self.request.FILES.getlist("files")
        print(docs)
        return super().perform_create(serializer)


class VehicleTypeView(generics.ListCreateAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer