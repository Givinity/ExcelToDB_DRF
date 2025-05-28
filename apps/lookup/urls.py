from django.urls import path, include

from apps.lookup.views import MaterialViewSet, CategoryViewSet, ImportView
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'material', MaterialViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('import/', ImportView.as_view(), name='import_xls'),
]
