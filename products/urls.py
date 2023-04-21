from rest_framework import routers
from django.urls import path, include
from .views import ProductViewSet,StockViewSet
router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
