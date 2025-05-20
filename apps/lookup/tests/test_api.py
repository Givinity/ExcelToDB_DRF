from decimal import Decimal

import pytest
from rest_framework.test import APIClient
from apps.lookup.models import Category, Material
from openpyxl import Workbook
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_category_list():
    client = APIClient()
    create = client.post(path="/api/v1/category/", data={'name': 'test', 'code': 1234}, format='json')
    assert create.status_code == 201
    response = client.get("/api/v1/category/")
    assert response.status_code == 200
    assert response.data[0]['name'] == 'test'


@pytest.mark.django_db
def test_material_list():
    client = APIClient()
    cat = Category.objects.create(name='test', code=1234)
    create = client.post(path="/api/v1/material/", data={'name': 'test_mat', 'code': 4321, 'cost': 123, 'cat': cat.id},
                         format='json')
    assert create.status_code == 201
    response = client.get("/api/v1/material/")
    assert response.status_code == 200
    assert response.data[0]['name'] == 'test_mat'


@pytest.mark.django_db
def test_import_xls_view():
    # Создаем временную Excel-книгу
    wb = Workbook()
    ws = wb.active
    ws.append(["Код категории", "Имя категории", "Род. категория", "Код материала", "Имя материала", "Стоимость"])
    ws.append([1001, "Категория A", None, None, None, None])  # категория
    ws.append([1001, "Категория A", None, 2001, "Материал A", 999.99])  # материал

    from io import BytesIO
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    django_file = SimpleUploadedFile("test.xlsx", excel_file.read(),
                                     content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    client = APIClient()
    response = client.post("/api/v1/category/import_xls/", {'file': django_file}, format='multipart')

    assert response.status_code == 200
    assert response.data == "Импорт завершен"

    category = Category.objects.first()
    assert category.name == "Категория A"

    material = Material.objects.first()
    assert material.name == "Материал A"
    assert material.cost == Decimal('999.99')
