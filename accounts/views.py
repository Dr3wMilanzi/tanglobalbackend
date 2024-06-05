from rest_framework import viewsets,generics
from .models import CompanyContactDetails
from .serializers import CompanyContactDetailsSerializer


class CompanyCreateList(generics.ListCreateAPIView):
    queryset = CompanyContactDetails.objects.all()
    serializer_class = CompanyContactDetailsSerializer


class CompanyRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyContactDetails.objects.all()
    serializer_class = CompanyContactDetailsSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


