from rest_framework import serializers
from apps.lookup.models import Category, Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('name', 'cat', 'code', 'cost')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'code', 'parent_cat')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'cat', 'code', 'cost']


class FlatSerializers(serializers.ModelSerializer):
    """"Вывод одномерным списком в json"""
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'materials']


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Рекурсивный сериализатор для иерархического дерева категорий"""
    children = serializers.SerializerMethodField()
    materials = MaterialSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'children', 'total_cost', 'materials', ]

    def get_children(self, obj):
        children = obj.children.all()
        if not children:
            return []
        return CategoryTreeSerializer(children, many=True).data