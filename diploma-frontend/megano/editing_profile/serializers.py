from rest_framework import serializers

from authentication.models import Profile


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'avatar',
        )
