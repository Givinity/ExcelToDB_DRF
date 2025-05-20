from django.urls import path

from apps.lookup.views import MaterialAPIView, CatergoryAPIView

urlpatterns = [
    path('material/', MaterialAPIView.as_view()),
    path('category/', CatergoryAPIView.as_view())
]