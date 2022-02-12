from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(required=False, many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def validate(self, attrs):
        attrs_list = [product['product'] for product in attrs['positions']]
        attrs_set = {product['product'] for product in attrs['positions']}

        if len(attrs_list) != len(attrs_set):
            raise ValidationError('Products cannot be duplicated')

        return attrs


    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for p in positions:
            StockProduct.objects.create(stock=stock, **p)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for p in positions:
            StockProduct.objects.update_or_create(stock=stock, product=p['product'], defaults={**p})

        return stock
