from rest_framework import generics, status
from rest_framework.response import Response
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
    lookup_field = 'slug'

class UserSelectedUpdatesList(generics.ListAPIView):
    serializer_class = UpdateSerializer

    def get_queryset(self):
        user = self.request.user
        selected_updates = SelectedUpdatesByUser.objects.filter(user=user)
        selected_update_type_ids = selected_updates.values_list('update_type__id', flat=True)
        queryset = Update.objects.filter(update_type__id__in=selected_update_type_ids)
        return queryset

class UserSubscriptionList(generics.ListCreateAPIView):
    serializer_class = SelectedUpdatesByUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SelectedUpdatesByUser.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        update_type_ids = request.data.get('update_types', [])
        if not isinstance(update_type_ids, list):
            return Response({'error': 'update_types must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.request.user
        SelectedUpdatesByUser.objects.filter(user=user).delete()
        
        for update_type_id in update_type_ids:
            try:
                update_type = UpdateType.objects.get(id=update_type_id)
                SelectedUpdatesByUser.objects.create(user=user, update_type=update_type)
            except UpdateType.DoesNotExist:
                return Response({'error': f'UpdateType with id {update_type_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

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

class ApproveUpdateView(generics.UpdateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_approved = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
