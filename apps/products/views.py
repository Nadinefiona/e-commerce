from django.core.cache import cache
from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from apps.accounts.permissions import IsVendor
from apps.products.models import Category, Product
from apps.products.serializers import CategorySerializer, ProductSerializer

PRODUCT_LIST_CACHE_KEY = "product_list"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ["category", "is_active", "vendor"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Product.objects.select_related("vendor", "category").all()

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsVendor()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_key = f"{PRODUCT_LIST_CACHE_KEY}:{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response, timeout=120)
        return response

    def perform_update(self, serializer):
        serializer.save()
        cache.delete_pattern(f"{PRODUCT_LIST_CACHE_KEY}:*") if hasattr(cache, "delete_pattern") else None

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete_pattern(f"{PRODUCT_LIST_CACHE_KEY}:*") if hasattr(cache, "delete_pattern") else None
