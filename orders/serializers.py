from rest_framework import serializers
from .models import Order, OrderItem
from django.db import transaction
from users.models import MyUser


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=False
    )
    quantity = serializers.IntegerField(max_value=100, min_value=1)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]
        read_only_fields = ["order"]

    def validate_order(self, value):
        order_id = self.context["view"].kwargs.get("order_pk")
        if order_id and str(order_id) != str(value.id):
            value.id = int(order_id)
            # raise serializers.ValidationError("Invalid order")
        return value


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=MyUser.objects.all())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "customer", "ordered_date", "status", "order_items")

    def create(self, validated_data):
        with transaction.atomic():
            order_items_data = validated_data.pop("order_items")
            order = Order.objects.create(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
        return order

    def validate(self, attrs):
        order_items = attrs.get("order_items")
        if not order_items:
            raise serializers.ValidationError(
                {"order_items": "Order items must not be empty"})
        return attrs
