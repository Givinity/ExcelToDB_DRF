import pytest
from apps.lookup.models import Category, Material


@pytest.mark.django_db
def test_category_create():
    cat = Category.objects.create(name='test', code=1234)
    assert cat.name == 'test'
    assert cat.code == 1234


@pytest.mark.django_db
def test_material_create():
    cat = Category.objects.create(name='test', code=1234)
    mat = Material.objects.create(name='test_mat', code=4321, cost=123, cat=cat)
    assert mat.name == 'test_mat'
    assert mat.code == 4321
    assert mat.cost == 123
