from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CargoType, Cargo, CargoDocument, CargoImage, CargoTracking
from .serializers import CargoTypeSerializer, CargoSerializer, CargoDocumentSerializer, CargoImageSerializer, CargoTrackingSerializer

class CargoTypeViewSet(viewsets.ModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    lookup_field = 'slug'

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['post'])
    def set_status_pending(self, request, slug=None):
        cargo = self.get_object()
        cargo.set_status_pending()
        return Response({'status': 'status set to pending'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_status_in_transit(self, request, slug=None):
        cargo = self.get_object()
        cargo.set_status_in_transit()
        return Response({'status': 'status set to in transit'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_status_delivered(self, request, slug=None):
        cargo = self.get_object()
        cargo.set_status_delivered()
        return Response({'status': 'status set to delivered'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_status_delayed(self, request, slug=None):
        cargo = self.get_object()
        cargo.set_status_delayed()
        return Response({'status': 'status set to delayed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_status_cancelled(self, request, slug=None):
        cargo = self.get_object()
        cargo.set_status_cancelled()
        return Response({'status': 'status set to cancelled'}, status=status.HTTP_200_OK)

class CargoDocumentViewSet(viewsets.ModelViewSet):
    queryset = CargoDocument.objects.all()
    serializer_class = CargoDocumentSerializer

class CargoImageViewSet(viewsets.ModelViewSet):
    queryset = CargoImage.objects.all()
    serializer_class = CargoImageSerializer

class CargoTrackingViewSet(viewsets.ModelViewSet):
    queryset = CargoTracking.objects.all()
    serializer_class = CargoTrackingSerializer