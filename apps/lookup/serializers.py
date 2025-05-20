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