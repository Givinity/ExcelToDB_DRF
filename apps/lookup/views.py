import openpyxl
from rest_framework import generics, viewsets, status
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


    @action(methods=['post'], detail=False)
    def import_xls(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response('Файл не найден или не передан')

        try:
            excel_file = openpyxl.open(file, read_only=True)

            sheet = excel_file.active
            max_rows = sheet.max_row

            for row in range(2, max_rows):
                code_cat = sheet[row][0].value # Код категории
                name_cat = sheet[row][1].value # Имя категории
                parent_cat = sheet[row][2].value # Род. категория
                code_mat = sheet[row][3].value # Код материала
                name_mat = sheet[row][4].value # Имя материала
                cost = sheet[row][5].value # Стоиимость

                if not name_cat or not code_cat:
                    return Response('Неверный файл Excel, имя категории должно быть обязательно заполнено')

                if name_cat and code_cat and not name_mat:
                    parent_cat_obj = None
                    parent_cat_obj = Category.objects.filter(name=parent_cat).first()
                    category, _ = Category.objects.update_or_create(
                        code = code_cat,
                        defaults= {
                            'name': name_cat,
                            'parent_cat': parent_cat_obj
                        }
                    )
                elif code_mat and name_mat and cost:
                    cat_obj = Category.objects.filter(name=name_cat).first()
                    Material.objects.update_or_create(
                        code = code_mat,
                        defaults= {
                            'name': name_mat,
                            'cat': cat_obj,
                            'cost': cost
                        }
                    )
            return Response('Импорт завершен' ,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(f'Ошибка: {e}', status=status.HTTP_400_BAD_REQUEST)