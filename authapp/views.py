from django.shortcuts import render

# Create your views here.

from rest_framework.request import Request
from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from authapp.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view

# Create your views here.


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super(UserView, self).get_permissions()

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request: Request) -> Response:
        # self.permission_classes = [AllowAny]

        serialized_data = UserSerializer(
            data=request.data, context={"request": request}
        )
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=201)
        return Response(serialized_data.errors, status=400)

    def get(self, request, *args, **kwargs):
        print("-->KWARGS<--", kwargs)
        print("-->ARGS<--", args)
        if "user_id" in kwargs:
            return self.get_single_user(request, kwargs["user_id"])
        else:
            return self.get_all_users(request)

    def get_single_user(self, request, user_id):
        """Fetch and return a single user based on the user_id"""
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        except CustomUser.DoesNotExist:
            return Response("User not found", status=404)

    def get_all_users(self, request):
        """Fetch and return all users paginated to 20 per request"""
        try:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            users = CustomUser.objects.all()
            result_page = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(result_page, many=True)
            return Response(serializer.data, status=200)
        except CustomUser.DoesNotExist:
            return Response("User not found", status=404)

    # create user update and logout and delete views
    def put(self, request, *args, **kwargs):
        if "user_id" in kwargs:
            try:
                user = CustomUser.objects.get(id=kwargs["user_id"])
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            except CustomUser.DoesNotExist:
                return Response("User not found", status=404)
        return Response("User ID is required", status=400)

    def delete(self, request, *args, **kwargs):
        if "user_id" in kwargs:
            try:
                user = CustomUser.objects.get(id=kwargs["user_id"])
                user.delete()
                return Response("User deleted successfully", status=200)
            except CustomUser.DoesNotExist:
                return Response("User not found", status=404)
        return Response("User ID is required", status=400)

    def logout(self, request, *args, **kwargs):
        if "user_id" in kwargs:
            try:
                user = CustomUser.objects.get(id=kwargs["user_id"])
                user.delete()
                return Response("User logged out successfully", status=200)
            except CustomUser.DoesNotExist:
                return Response("User not found", status=404)
        return Response("User ID is required", status=400)
