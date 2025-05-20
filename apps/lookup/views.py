from rest_framework import generics
from apps.lookup.models import Category, Material
from apps.lookup.serializers import MaterialSerializer, CategorySerializer


class MaterialAPIView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class CatergoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
