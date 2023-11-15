import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from orders.models import Order


@api_view(http_method_names=['post', 'get'])
def payment(request: Request, *args, **kwargs) -> Response:
    order = Order.objects.get(id=kwargs['id'])
    list_of_errors = ['Слишком мало средств', 'Слишком много средств', 'Товар закончился',
                      'Мы вам ничего не продадим', 'Даже не пытайтесь', 'Ошибка']

    if request.method == 'POST':
        number = int(request.data['number'])

        if (number % 2 == 0) and (number % 10 != 0):
            order.status = 'Оплачено'
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            error = random.choice(list_of_errors)
            order.status = f'Ошибка: {error}'
            order.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)
