# Create serializer for User model

#         """Fetch and return all users paginated to 20 per request"""


from authapp.models import CustomUser
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = "__all__"
        fields = [
            f.name
            for f in CustomUser._meta.fields
            if f.name
            not in [
                "is_superuser",
                "is_staff",
                "is_active",
                "groups",
                "user_permissions",
            ]
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
