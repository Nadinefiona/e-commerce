from rest_framework import serializers

from apps.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default=None)
    vendor_name = serializers.CharField(source="vendor.username", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "vendor", "vendor_name", "category", "category_name",
            "name", "slug", "description", "price", "stock",
            "image", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "vendor", "created_at", "updated_at"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
