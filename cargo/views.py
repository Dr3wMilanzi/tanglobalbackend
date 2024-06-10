from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Cargo, CargoType,CargoDocument
from .serializers import CargoSerializer, CargoTypeSerializer
from rest_framework.permissions import IsAuthenticated


class CargoListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
        # docs = self.request.FILES.getlist("cargo_documents")
        # print(docs)
        # payload = self.request.data
        # print("Payload:", payload)
        # return super().perform_create(serializer)
        
        # cargo_documents = self.request.FILES.getlist('cargo_documents')
        # cargo_document_names = self.request.POST.getlist('cargo_document_names')
        # print(cargo_documents)
        # cargo = serializer.save(sender_name=self.request.user)

        # for i, document in enumerate(cargo_documents):
        #     document_name = cargo_document_names[i] if i < len(cargo_document_names) else ''
        #     CargoDocument.objects.create(cargo=cargo, documentFile=document, documentName=document_name)



class CargoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'


class CargoCartegoriesCreateAPIView(generics.ListCreateAPIView):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer


class CargoByCategoryAPIView(generics.ListCreateAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()

    def perform_create(self, serializer):
        cargo_documents_data = self.request.data.pop('cargo_documents', [])
        print(cargo_documents_data)
        # # cargo_type = self.request.data.pop('cargo_type', None)

        # # for document_data in cargo_documents_data:
        # #     CargoDocument.objects.create(cargo=cargo, **document_data)
        # serializer.save(sender_name=self.request.user)


