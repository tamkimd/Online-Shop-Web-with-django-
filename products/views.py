from rest_framework import viewsets, filters
from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly



class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'name', 'id']  # ?ordering=-price
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        print(self.request.user)
        if self.action == 'list' or self.request.user.is_staff:
            return Product.objects.all()
        else:
            return Product.objects.none()
