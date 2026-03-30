from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart, CartItem
from apps.cart.serializers import CartItemSerializer, CartSerializer
from apps.products.models import Product


class CartDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.prefetch_related("items__product").get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)


class CartItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({"detail": "This product does not exist or is unavailable."}, status=status.HTTP_404_NOT_FOUND)

        if quantity < 1:
            return Response({"detail": "Quantity must be at least 1."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity > product.stock:
            return Response({"detail": f"Only {product.stock} items available in stock."}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            item.quantity = quantity
            item.save()

        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.data.get("product")
        deleted, _ = CartItem.objects.filter(cart__user=request.user, product_id=product_id).delete()
        if not deleted:
            return Response({"detail": "This item is not in your cart."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Item removed from cart."}, status=status.HTTP_200_OK)
