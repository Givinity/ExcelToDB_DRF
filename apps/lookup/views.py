from apps.lookup.services.import_xls import ImportService
from django.db import transaction
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from apps.lookup.models import Category, Material
from apps.lookup.serializers import MaterialSerializer, CategorySerializer, FlatSerializers, CategoryTreeSerializer, ImportSerializer
from rest_framework.decorators import action


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=False)
    def flat(self, request):
        categories = Category.objects.all()
        # flat = [cat.name for cat in categories]
        serializer_class = FlatSerializers(categories, many=True)
        return Response(serializer_class.data)

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


class ImportView(generics.CreateAPIView):
    serializer_class = ImportSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response('Файл не найден или не передан', status.HTTP_400_BAD_REQUEST)

        import_result = ImportService.import_xls(file)

        if import_result == 'import done':
            return Response('Импорт завершен', status.HTTP_200_OK)
        else:
            return Response(import_result, status.HTTP_400_BAD_REQUEST)
