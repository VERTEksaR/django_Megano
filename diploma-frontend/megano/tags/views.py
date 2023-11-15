from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tags


class TagsAPIView(APIView):
    def get(self, request: Request) -> Response:
        data = []
        queryset = Tags.objects.all()
        for tag in queryset:
            list_of_data = {
                'id': tag.pk,
                'name': tag.name,
            }
            data.append(list_of_data)
        return Response(data)

    def post(self, request: Request) -> Response:
        name = request.data['name']
        Tags.objects.create(name=name)
        return Response(status=status.HTTP_200_OK)
