from datetime import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, ProductsInOrder, Delivery, Payment
from products.models import Product, ImageForProduct, ReviewForProduct
from authentication.models import Profile
from basket.models import BasketModel


class OrderAPIView(APIView):
    def get(self, request: Request) -> Response:
        list_of_orders = []
        orders = Order.objects.select_related('user').filter(user=request.user)
        product_orders = ProductsInOrder.objects.select_related('order', 'product').all()
        products_images = ImageForProduct.objects.select_related('product').all()
        products_reviews = ReviewForProduct.objects.select_related('product').all()

        for order in orders:
            products_list = []

            for product_in_order in product_orders.filter(order=order):
                product = product_in_order.product
                product_images = products_images.filter(product=product)
                product_reviews = products_reviews.filter(product=product)

                images, tags = [], []
                all_rating, rating, count = 0, 0, 0

                if product_images:
                    for image in product_images:
                        images.append(image.info_image())

                if product.tags.filter(product=product).all():
                    for tag in product.tags.filter(product=product).all():
                        tags.append(str(tag))

                if product_reviews:
                    for review in product_reviews:
                        all_rating += review.rate
                        count += 1
                    rating = all_rating / count

                product_data = {
                    'id': product.pk,
                    'category': product.category.pk,
                    'price': product.price,
                    'count': product_in_order.count,
                    'date': product.date,
                    'title': product.title,
                    'description': product.description,
                    'freeDelivery': product.freeDelivery,
                    'images': images,
                    'tags': tags,
                    'reviews': count,
                    'rating': rating,
                }
                products_list.append(product_data)

            order_data = {
                'id': order.pk,
                'createdAt': order.createdAd,
                'fullName': order.fullName,
                'email': order.email,
                'phone': order.phone,
                'deliveryType': order.deliveryType.type,
                'paymentType': order.paymentType.type,
                'totalCost': order.totalCost,
                'status': order.status,
                'city': order.city,
                'address': order.address,
                'products': products_list,
            }
            list_of_orders.append(order_data)
        return Response(list_of_orders)

    def post(self, request: Request) -> Response:
        print(request.data)
        total_price = 0
        user = Profile.objects.only('fullname', 'email', 'phone').filter(user=self.request.user)[0]
        delivery_type = Delivery.objects.filter(type='ordinary')
        payment_type = Payment.objects.filter(type='online')

        for product_count in request.data:
            product = (Product.objects.only('count', 'purchases')
                       .get(id=product_count['id']))
            count = product_count['count']
            if count > product.count:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            product.count -= count
            product.purchases += count
            product.save(update_fields=['count', 'purchases'])

        for product_price in request.data:
            count = product_price['count']
            total_price += product_price['price'] * count

        order = Order.objects.create(
            user=request.user, totalCost=total_price, fullName=user.fullname,
            email=user.email, phone=user.phone, deliveryType=delivery_type[0],
            paymentType=payment_type[0]
        )

        for product in request.data:
            product_id = product['id']
            product_count = product['count']
            needed_product = (Product.objects.select_related('category')
                              .prefetch_related('tags').filter(id=product_id))
            ProductsInOrder.objects.create(
                order=order, product=needed_product[0], count=product_count
            )

        users_basket = BasketModel.objects.filter(user=request.user)
        users_basket.delete()
        return Response(status=status.HTTP_200_OK)


class OneOrderAPIView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        products_list = []
        order_id = kwargs['id']
        order = Order.objects.select_related('user').filter(id=order_id)[0]
        product_orders = ProductsInOrder.objects.select_related('order', 'product').filter(order=order)
        products_images = ImageForProduct.objects.select_related('product').all()
        products_reviews = ReviewForProduct.objects.select_related('product').all()

        for product_in_order in product_orders.filter(order=order):
            product = product_in_order.product
            product_images = products_images.filter(product=product)
            product_reviews = products_reviews.filter(product=product)

            images, tags = [], []
            all_rating, rating, count = 0, 0, 0

            if product_images:
                for image in product_images:
                    images.append(image.info_image())

            if product.tags.filter(product=product).all():
                for tag in product.tags.filter(product=product).all():
                    tags.append(str(tag))

            if product_reviews:
                for review in product_reviews:
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
                'count': product_in_order.count,
                'date': product.date,
                'title': product.title,
                'description': product.description,
                'freeDelivery': product.freeDelivery,
                'images': images,
                'tags': tags,
                'reviews': count,
                'rating': rating,
            }
            products_list.append(product_data)

        order_data = {
            'id': order.pk,
            'createdAt': order.createdAd,
            'fullName': order.fullName,
            'email': order.email,
            'phone': order.phone,
            'deliveryType': order.deliveryType.type,
            'paymentType': order.paymentType.type,
            'totalCost': order.totalCost,
            'status': order.status,
            'city': order.city,
            'address': order.address,
            'products': products_list,
        }

        return Response(order_data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        order = Order.objects.get(id=request.data['orderId'])
        deliveryType = request.data['deliveryType']
        city = request.data['city']
        address = request.data['address']
        paymentType = request.data['paymentType']

        delivery = Delivery.objects.get(type=deliveryType)
        payment = Payment.objects.get(type=paymentType)

        order.deliveryType, order.city, order.address = delivery, city, address
        order.paymentType = payment

        if delivery.type == 'express':
            order.totalCost += delivery.tax
        elif delivery.type == 'ordinary':
            if order.totalCost < delivery.freePrice:
                order.totalCost += delivery.tax

        if not order.fullName:
            fullName = request.data['fullName']
            phone = request.data['phone']
            email = request.data['email']

            order.fullName, order.phone, order.email = fullName, phone, email
            order.save(update_fields=['fullName', 'phone', 'email', 'totalCost',
                                      'deliveryType', 'city', 'address', 'paymentType'])
            return Response(status=status.HTTP_200_OK)

        order.save(update_fields=['deliveryType', 'city', 'address', 'paymentType', 'totalCost'])
        return Response({"orderId": kwargs['id']}, status=status.HTTP_200_OK)
