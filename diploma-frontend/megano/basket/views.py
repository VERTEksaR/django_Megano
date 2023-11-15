from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BasketModel
from products.models import Product, ImageForProduct, ReviewForProduct


class BasketAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        products_data = []
        basket = BasketModel.objects.select_related('product', 'user').filter(user=request.user)
        product_images = ImageForProduct.objects.select_related('product').all()
        products_reviews = ReviewForProduct.objects.select_related('product').all()

        if basket:
            for product_in_basket in basket:
                product_queryset = (Product.objects
                                    .select_related('category')
                                    .prefetch_related('tags')
                                    .filter(title=product_in_basket))
                product = product_queryset[0]
                images, tags = [], []
                all_rating, rating, count = 0, 0, 0

                if product_images.filter(product=product):
                    for image in product_images.filter(product=product):
                        images.append(image.info_image())

                if product.tags.filter(product=product).all():
                    for tag in product.tags.filter(product=product).all():
                        tags.append(str(tag))

                if products_reviews.filter(product=product):
                    for review in products_reviews.filter(product=product):
                        all_rating += review.rate
                        count += 1
                    rating = all_rating / count

                data = {
                    'id': product.pk,
                    'category': product.category.pk,
                    'price': product.price,
                    'count': product_in_basket.count,
                    'date': product.date,
                    'title': product.title,
                    'description': product.description,
                    'freeDelivery': product.freeDelivery,
                    'images': images,
                    'tags': tags,
                    'reviews': count,
                    'rating': rating,
                }
                products_data.append(data)

            return Response(products_data)
        return Response(status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        product_id = request.data['id']
        count = request.data['count']
        user = request.user
        product = (Product.objects.select_related('category')
                   .prefetch_related('tags')
                   .filter(id=product_id))
        product_in_basket, create = BasketModel.objects.get_or_create(
            product=product[0], user=user
        )

        if not create:
            product_in_basket.count += count
            product_in_basket.save(update_fields=['count'])
        else:
            product_in_basket.count = count
            product_in_basket.save(update_fields=['count'])

        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        product_id = request.data['id']
        product_count = request.data['count']
        product = Product.objects.select_related('category').prefetch_related('tags').filter(pk=product_id)
        product_in_basket = BasketModel.objects.get(user=request.user, product=product[0])

        if product_count < product_in_basket.count:
            product_in_basket.count -= product_count
            product_in_basket.save(update_fields=['count'])
        elif product_count == product_in_basket.count:
            product_in_basket.delete()

        return Response(status=status.HTTP_200_OK)
