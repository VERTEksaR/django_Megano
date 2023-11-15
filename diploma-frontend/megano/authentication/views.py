import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Profile


@api_view(http_method_names=['post', 'get'])
def sign_up(request: Request) -> Response:
    if request.method == 'POST':
        info = json.loads(request.body)
        name = info['name']
        username = info['username']
        password = info['password']

        user = User.objects.create_user(
            first_name=name,
            username=username,
            password=password,
        )
        user.save()
        Profile.objects.create(fullname=name, user_id=user.pk)

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['post', 'get'])
def sign_in(request: Request) -> Response:
    if request.method == 'POST':
        info = json.loads(request.body)
        username = info['username']
        password = info['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['post', 'get'])
def sign_out(request: Request) -> Response:
    if request.method == 'POST':
        logout(request)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


