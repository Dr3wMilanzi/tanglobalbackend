# views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UpdateType, Update, SelectedUpdatesByUser, UpdateView
from .serializers import UpdateTypeSerializer, UpdateSerializer, SelectedUpdatesByUserSerializer, UpdateViewSerializer

class UpdateTypeList(generics.ListCreateAPIView):
    queryset = UpdateType.objects.all()
    serializer_class = UpdateTypeSerializer
    permission_classes = [IsAuthenticated]

class UpdateTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UpdateType.objects.all()
    serializer_class = UpdateTypeSerializer
    permission_classes = [IsAuthenticated]

class UpdateList(generics.ListCreateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UpdateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

class UserSubscriptionList(generics.ListCreateAPIView):
    serializer_class = SelectedUpdatesByUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SelectedUpdatesByUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserSubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SelectedUpdatesByUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SelectedUpdatesByUser.objects.filter(user=self.request.user)

class UpdateViewList(generics.ListCreateAPIView):
    queryset = UpdateView.objects.all()
    serializer_class = UpdateViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UpdateView.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UpdateView.objects.all()
    serializer_class = UpdateViewSerializer
    permission_classes = [IsAuthenticated]
