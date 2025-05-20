import pytest
from apps.lookup.models import Category, Material
from apps.lookup.serializers import FlatSerializers, CategoryTreeSerializer


@pytest.mark.django_db
def test_flat_serializer_with_materials():
    cat = Category.objects.create(name='test cat', code=1001)
    mat1 = Material.objects.create(name='mat_1', code=2001, cost=100, cat=cat)
    mat2 = Material.objects.create(name='mat_2', code=2002, cost=200, cat=cat)

    serializer = FlatSerializers(instance=cat)
    data = serializer.data

    assert data['name'] == 'test cat'
    assert len(data['materials']) == 2
    assert data['materials'][0]['name'] == 'mat_1'
    assert data['materials'][1]['name'] == 'mat_2'


@pytest.mark.django_db
def test_category_tree_serializer_with_children_and_materials():
    parent = Category.objects.create(name='Parent', code=1)
    child = Category.objects.create(name='Child', code=2, parent_cat=parent)
    Material.objects.create(name='mat Parent', code=111, cost=500, cat=parent)
    Material.objects.create(name='mat Child', code=222, cost=300, cat=child)

    serializer = CategoryTreeSerializer(instance=parent)
    data = serializer.data

    assert data['name'] == 'Parent'
    assert len(data['materials']) == 1
    assert data['materials'][0]['name'] == 'mat Parent'
    assert len(data['children']) == 1
    assert data['children'][0]['name'] == 'Child'
    assert len(data['children'][0]['materials']) == 1
    assert data['children'][0]['materials'][0]['name'] == 'mat Child'
