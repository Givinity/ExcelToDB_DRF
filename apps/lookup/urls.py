from django.urls import path, include

from apps.lookup.views import MaterialViewSet, CatergoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'material', MaterialViewSet)
router.register(r'category', CatergoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]