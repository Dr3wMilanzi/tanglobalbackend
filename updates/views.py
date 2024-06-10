# views.py

from rest_framework import generics
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
    lookup_field = 'slug'  #
    

class UserSelectedUpdatesList(generics.ListAPIView):
    serializer_class = UpdateSerializer

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # Get the selected update types for the current user
        selected_updates = SelectedUpdatesByUser.objects.filter(user=user)

        # Extract the IDs of the selected update types
        selected_update_type_ids = selected_updates.values_list('update_type__id', flat=True)

        # Get updates that belong to the selected update types
        queryset = Update.objects.filter(update_type__id__in=selected_update_type_ids)

        return queryset


class UserSubscriptionList(generics.ListCreateAPIView):
    serializer_class = SelectedUpdatesByUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch the selected update types for the current user
        return SelectedUpdatesByUser.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Override the list method to customize the response data
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        # Serialize the queryset and return the response
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        update_type_ids = request.data.get('update_types', [])
        
        if not isinstance(update_type_ids, list):
            return Response({'error': 'update_types must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.request.user
        
        # Remove existing selections for the current user
        SelectedUpdatesByUser.objects.filter(user=user).delete()
        
        # Create new selections for the update types
        for update_type_id in update_type_ids:
            try:
                update_type = UpdateType.objects.get(id=update_type_id)
                SelectedUpdatesByUser.objects.create(user=user, update_type=update_type)
            except UpdateType.DoesNotExist:
                return Response({'error': f'UpdateType with id {update_type_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    
       
class UserSelectedUpdatesList(generics.ListAPIView):
    serializer_class = UpdateSerializer

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # Get the selected update types for the current user
        selected_updates = SelectedUpdatesByUser.objects.filter(user=user)

        # Extract the IDs of the selected update types
        selected_update_type_ids = selected_updates.values_list('update_type__id', flat=True)

        # Get updates that belong to the selected update types
        queryset = Update.objects.filter(update_type__id__in=selected_update_type_ids)

        return queryset
    

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
