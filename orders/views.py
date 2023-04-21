
from django.conf import settings
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import (

    OrderSerializer,
    OrderItemSerializer,
)
from products.models import Product, Stock
from rest_framework.decorators import action

from django.core.mail import send_mail
from django.db import transaction


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return self.queryset.filter(order=self.kwargs.get("order_pk"))


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def confirm_order(self, request, pk=None):
        order = self.get_object()
        order.status = "confrimed"
        order.save()
        order_items = order.order_items.all()
        for item in order_items:
            product = item.product
            quantity = item.quantity
            stock = Stock.objects.get(product=product)
            stock.quantity -= quantity
            stock.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def shipped_order(self, request, pk=None):
        order = self.get_object()
        order.status = "shipped"
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def send_mail(self, request, pk=None):
        order = self.get_object()
        customer = order.customer
        order_items = order.order_items.all()
        total_price = 0
        product_quantities = {}

        for item in order_items:
            total_price += item.product.price * (item.quantity)
            
            if item.product.id not in product_quantities:
                product_quantities[item.product.id] = item.quantity
            else:
                product_quantities[item.product.id] += item.quantity

        # Create the message object
        message = f"Hello {customer.name},\n\n"
        message += "Thank you for your order!\n\n"
        message += "Here are your order details:\n\n"
        message += "Product Name\tQuantity\n"
        
        for product_id, quantity in product_quantities.items():
            product_name = Product.objects.get(id=product_id).name
            message += f"{product_name}\t{quantity}\n"

        message += f"\nTotal Price: {total_price} vnd\n\n"
        message += "Thank you for shopping with us!"

        send_mail(
            "Your order confirmation",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [customer.email],
            fail_silently=False,
        )

        return Response({"status": "Email sent."})
