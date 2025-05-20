from rest_framework import generics, viewsets
from rest_framework.response import Response

from apps.lookup.models import Category, Material
from apps.lookup.serializers import MaterialSerializer, CategorySerializer, FlatSerializers, CategoryTreeSerializer
from rest_framework.decorators import action


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class CatergoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=False)
    def flat(self, request):
        categories = Category.objects.all()
        # flat = [cat.name for cat in categories]
        serializer_class = FlatSerializers(categories, many=True)
        return Response(serializer_class)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Отображение категорий в виде иерархического дерева с материалами
        и расчетом суммарной стоимости для каждой категории
        """
        # Получаем только корневые категории (без родителей)
        root_categories = Category.objects.filter(parent_cat=None)
        serializer = CategoryTreeSerializer(root_categories, many=True)
        return Response(serializer.data)