# views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CargoType, Cargo, CargoDocument, CargoImage, CargoTracking
from .serializers import CargoTypeSerializer, CargoSerializer, CargoDocumentSerializer, CargoImageSerializer, CargoTrackingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

class CargoTypeViewSet(viewsets.ModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    lookup_field = 'slug'

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        cargo = serializer.save(sender_name=self.request.user)
        for document in self.request.FILES.getlist('documents'):
            CargoDocument.objects.create(cargo=cargo, file=document)
        for image in self.request.FILES.getlist('images'):
            CargoImage.objects.create(cargo=cargo, image=image)

    def perform_update(self, serializer):
        cargo = serializer.save()
        cargo.cargo_documents.all().delete()
        cargo.images.all().delete()
        for document in self.request.FILES.getlist('documents'):
            CargoDocument.objects.create(cargo=cargo, file=document)
        for image in self.request.FILES.getlist('images'):
            CargoImage.objects.create(cargo=cargo, image=image)

    @action(detail=True, methods=['post'])
    def set_status_pending(self, request, slug=None):
        with transaction.atomic():
            cargo = self.get_object()
            if cargo.status not in ['in_transit', 'delivered', 'delayed', 'cancelled']:
                cargo.status = 'pending'
                cargo.save()
                logger.info(f"Cargo {cargo.slug} status set to pending by {request.user}")
                return Response({'status': 'status set to pending'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status transition'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_status_in_transit(self, request, slug=None):
        with transaction.atomic():
            cargo = self.get_object()
            if cargo.status == 'pending':
                cargo.status = 'in_transit'
                cargo.save()
                logger.info(f"Cargo {cargo.slug} status set to in transit by {request.user}")
                return Response({'status': 'status set to in transit'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status transition'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_status_delivered(self, request, slug=None):
        with transaction.atomic():
            cargo = self.get_object()
            if cargo.status == 'in_transit':
                cargo.status = 'delivered'
                cargo.save()
                logger.info(f"Cargo {cargo.slug} status set to delivered by {request.user}")
                return Response({'status': 'status set to delivered'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status transition'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_status_delayed(self, request, slug=None):
        with transaction.atomic():
            cargo = self.get_object()
            if cargo.status in ['pending', 'in_transit']:
                cargo.status = 'delayed'
                cargo.save()
                logger.info(f"Cargo {cargo.slug} status set to delayed by {request.user}")
                return Response({'status': 'status set to delayed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status transition'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_status_cancelled(self, request, slug=None):
        with transaction.atomic():
            cargo = self.get_object()
            if cargo.status in ['pending', 'in_transit', 'delayed']:
                cargo.status = 'cancelled'
                cargo.save()
                logger.info(f"Cargo {cargo.slug} status set to cancelled by {request.user}")
                return Response({'status': 'status set to cancelled'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status transition'}, status=status.HTTP_400_BAD_REQUEST)

class CargoDocumentViewSet(viewsets.ModelViewSet):
    queryset = CargoDocument.objects.all()
    serializer_class = CargoDocumentSerializer

class CargoImageViewSet(viewsets.ModelViewSet):
    queryset = CargoImage.objects.all()
    serializer_class = CargoImageSerializer

class CargoTrackingViewSet(viewsets.ModelViewSet):
    queryset = CargoTracking.objects.all()
    serializer_class = CargoTrackingSerializer
