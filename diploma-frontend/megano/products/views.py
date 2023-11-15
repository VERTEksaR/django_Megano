from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ImageForProduct, SpecificationsForProduct, ReviewForProduct


class ProductsAPIView(APIView):
    def get(self, request: Request, id) -> Response:
        product_data = {}
        product_query = Product.objects.select_related('category').prefetch_related('tags').filter(id=id)
        images, tags, specs, reviews = [], [], [], []
        all_rating, rating, count = 0, 0, 0

        if product_query:
            product = product_query[0]
            product_images = ImageForProduct.objects.filter(product=product).all()
            product_specifications = SpecificationsForProduct.objects.filter(product=product).all()
            product_reviews = ReviewForProduct.objects.filter(product=product).all()

            if product_images:
                for image in product_images:
                    images.append(image.info_image())

            if product.tags.all():
                for tag in product.tags.all():
                    tags.append(str(tag))

            if product_specifications:
                for spec in product_specifications:
                    spec_value = {
                        'name': spec.name,
                        'value': spec.value,
                    }
                    specs.append(spec_value)

            if product_reviews:
                for review in product_reviews:
                    review_value = {
                        'author': review.author,
                        'email': review.email,
                        'text': review.text,
                        'rate': review.rate,
                        'date': review.date,
                    }
                    reviews.append(review_value)

                    all_rating += review.rate
                    count += 1
                rating = all_rating / count

            day = datetime.now().strftime('%d')
            month = datetime.now().strftime('%m')

            if product.onSales:
                if (int(day) in range(int(datetime.strftime(product.dateFrom, '%d')),
                                      int(datetime.strftime(product.dateTo, '%d')) + 1)) and \
                        (int(month) in range(int(datetime.strftime(product.dateFrom, '%m')),
                                             int(datetime.strftime(product.dateTo, '%m')) + 1)):
                    product_price = product.salePrice
                else:
                    product_price = product.price
            else:
                product_price = product.price

            product_data = {
                'id': product.pk,
                'category': product.category.pk,
                'price': product_price,
                'count': product.count,
                'date': product.date,
                'title': product.title,
                'description': product.description,
                'fullDescription': product.fullDescription,
                'freeDelivery': product.freeDelivery,
                'images': images,
                'tags': tags,
                'reviews': reviews,
                'specifications': specs,
                'rating': rating,
            }
        return Response(product_data)


class ReviewAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, id) -> Response:
        queryset = ReviewForProduct.objects.all()
        product = Product.objects.select_related('category').prefetch_related('tags').filter(id=id)
        list_of_data = []

        if queryset:
            for review in queryset:
                if review.product.title == product[0].title:
                    data = {
                        'author': review.author,
                        'email': review.email,
                        'text': review.text,
                        'rate': review.rate,
                        'date': review.date,
                    }
                    list_of_data.append(data)
        return Response(list_of_data)

    def post(self, request: Request, id) -> Response:
        author = request.data['author']
        users_email = request.data['email']
        text = request.data['text']
        rate = request.data['rate']
        product = Product.objects.select_related('category').prefetch_related('tags').filter(id=self.kwargs['id'])
        review = ReviewForProduct.objects.create(
            author=author, email=users_email,
            text=text, rate=rate,
            product=product[0]
        )
        review.save()
        return Response(status=status.HTTP_200_OK)
