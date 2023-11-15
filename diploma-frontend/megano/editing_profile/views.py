from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Profile
from .serializers import ChangePasswordSerializer, AvatarSerializer


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        queryset = request.user.profile
        list_of_data = {
            'fullName': queryset.fullname,
            'phone': queryset.phone,
            'email': queryset.email,
            'avatar': queryset.info_avatar(),
        }
        return Response(list_of_data)

    def post(self, request: Request) -> Response:
        fullName = request.data['fullName']
        phone = request.data['phone']
        email = request.data['email']
        user = Profile.objects.get(user=request.user)
        user.fullname, user.phone, user.email = fullName, phone, email
        user.save(update_fields=['fullname', 'phone', 'email'])
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def post(self, request: Request, *args, **kwargs) -> Response:
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data['currentPassword']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data['newPassword'])
            self.object.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(status=status.HTTP_200_OK)


class ChangeAvatarView(UpdateAPIView):
    serializer_class = AvatarSerializer
    model = Profile
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def post(self, request: Request, *args, **kwargs) -> Response:
        formaters = ['jpg', 'jpeg', 'png']
        user = self.get_object()
        image = request.FILES['avatar']
        for form in formaters:
            if form in str(image):
                if image.size <= 2 * 1024 * 1024:
                    user.avatar = image
                    user.save(update_fields=['avatar'])
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request) -> Response:
        user = self.get_queryset()
        for profile_data in user:
            info = {
                'avatar': profile_data.info_avatar(),
            }
            return Response(info)

    def get_queryset(self):
        return Profile.objects.only('avatar').filter(user=self.request.user)
