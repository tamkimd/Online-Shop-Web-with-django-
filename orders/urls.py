from rest_framework import routers
from django.urls import path, include
from .views import OrderViewSet, OrderItemViewSet

router = routers.DefaultRouter()

router.register(r'orders', OrderViewSet)
router.register(r'orders/(?P<order_pk>\d+)/order_items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
