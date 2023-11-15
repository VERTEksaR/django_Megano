from datetime import datetime
from django.http import QueryDict
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from operator import itemgetter

from .models import Categories
from products.models import Product, ImageForProduct, SpecificationsForProduct, ReviewForProduct
from .pagination import PaginationCatalog


def getting_products(products):
    products_images = ImageForProduct.objects.select_related('product').all()
    products_reviews = ReviewForProduct.objects.select_related('product').all()
    list_of_products = []

    for product in products:
        images, tags = [], []
        all_rating, rating, count = 0, 0, 0

        if products_images.filter(product=product):
            for image in products_images.filter(product=product):
                images.append(image.info_image())

        if product.tags.filter(product=product).all():
            for tag in product.tags.filter(product=product).all():
                tags.append(str(tag))

        if products_reviews.filter(product=product):
            for review in products_reviews.filter(product=product):
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
            'freeDelivery': product.freeDelivery,
            'images': images,
            'tags': tags,
            'reviews': count,
            'rating': rating,
        }

        list_of_products.append(product_data)
    return list_of_products


class CategoriesAPIView(APIView):
    def get(self, request: Request) -> Response:
        main_data, list_of_ids = [], []
        categories = Categories.objects.all()

        for category in categories:
            subcategories = Categories.objects.filter(parent=category).all()
            sub_data = []

            if not category.parent:
                for subcategory in subcategories:
                    sub_list_of_data = {
                        'id': subcategory.pk,
                        'title': subcategory.title,
                        'image': subcategory.info_image(),
                    }
                    sub_data.append(sub_list_of_data)
                    list_of_ids.append(subcategory.pk)

            if category.pk not in list_of_ids:
                main_list_of_data = {
                    'id': category.pk,
                    'title': category.title,
                    'image': category.info_image(),
                    'subcategories': sub_data,
                }
                main_data.append(main_list_of_data)
                list_of_ids.append(category.pk)
        return Response(main_data)


class CatalogAPIList(ListAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('tags').all()

    def get(self, request: Request, *args, **kwargs) -> Response:

        query_params = QueryDict(request.GET.urlencode())

        filtered_items = self.queryset.all()
        items = []

        name = query_params.get('filter[name]')
        min_price = query_params.get('filter[minPrice]')
        max_price = query_params.get('filter[maxPrice]')
        free_delivery = query_params.get('filter[freeDelivery]')
        available = query_params.get('filter[available]')
        category = query_params.get('category')
        tags = query_params.getlist('tags[]')
        sort = query_params.get('sort')
        sort_type = query_params.get('sortType')

        if filtered_items:

            if name:
                filtered_items = filtered_items.filter(title__icontains=str(name))

            if min_price:
                filtered_items = filtered_items.filter(price__gte=min_price)

            if max_price:
                filtered_items = filtered_items.filter(price__lte=max_price)

            if free_delivery == 'true':
                filtered_items = filtered_items.filter(freeDelivery=True)
            else:
                filtered_items = filtered_items.filter(freeDelivery=False)

            if available == 'false':
                filtered_items = filtered_items.filter(count=0)

            if category:
                filtered_items = filtered_items.filter(category=category)

            if tags:
                for tag in tags:
                    filtered_items = filtered_items.filter(tags=tag)

            items = getting_products(filtered_items)

            if sort == 'rating':
                if sort_type == 'dec':
                    items = sorted(items, key=itemgetter('rating'))
                else:
                    items = sorted(items, key=itemgetter('rating'), reverse=True)
            elif sort == 'price':
                if sort_type == 'dec':
                    items = sorted(items, key=itemgetter('price'))
                else:
                    items = sorted(items, key=itemgetter('price'), reverse=True)
            elif sort == 'reviews':
                if sort_type == 'dec':
                    items = sorted(items, key=itemgetter('reviews'))
                else:
                    items = sorted(items, key=itemgetter('reviews'), reverse=True)
            elif sort == 'date':
                if sort_type == 'dec':
                    items = sorted(items, key=itemgetter('date'))
                else:
                    items = sorted(items, key=itemgetter('date'), reverse=True)

            paginator = PaginationCatalog()
            page = paginator.paginate_queryset(items, request)
            return paginator.get_paginated_response(page, len(items))
        return Response(items)


class PopularAPIView(APIView):
    def get(self, request: Request) -> Response:
        products = (Product.objects
                    .select_related('category')
                    .prefetch_related('tags')
                    .order_by('purchases', 'title'))[:8]
        list_of_products = []

        if products:
            list_of_products = getting_products(products)
        return Response(list_of_products)


class LimitedAPIView(APIView):
    def get(self, request: Request) -> Response:
        products = (Product.objects
                    .select_related('category')
                    .prefetch_related('tags')
                    .filter(limitedEdition=True))[:16]
        list_of_products = []

        if products:
            list_of_products = getting_products(products)
        return Response(list_of_products)


class BannersAPIView(APIView):
    def get(self, request: Request) -> Response:
        products = (Product.objects
                    .select_related('category')
                    .prefetch_related('tags')
                    .order_by('count'))[:3]
        list_of_products = []

        if products:
            list_of_products = getting_products(products)
        return Response(list_of_products)


class SalesAPIList(ListAPIView):
    queryset = Product.objects.only('price', 'salePrice', 'dateFrom', 'dateTo', 'onSales').filter(onSales=True)

    def get(self, request: Request, *args, **kwargs) -> Response:
        products = self.queryset.all()
        products_images = ImageForProduct.objects.select_related('product').filter(product__onSales=True)
        list_of_products = []

        if products:
            for product in products:
                images = []

                if products_images.filter(product=product):
                    for image in products_images.filter(product=product):
                        images.append(image.info_image())

                date_from = datetime.strftime(product.dateFrom, '%d-%m')
                date_to = datetime.strftime(product.dateTo, '%d-%m')

                product_data = {
                    'id': product.pk,
                    'price': product.price,
                    'salePrice': product.salePrice,
                    'dateFrom': date_from,
                    'dateTo': date_to,
                    'title': product.title,
                    'images': images,
                }
                list_of_products.append(product_data)

            paginator = PaginationCatalog()
            page = paginator.paginate_queryset(list_of_products, request)
            return paginator.get_paginated_response(page, len(list_of_products))
        return Response(list_of_products)
