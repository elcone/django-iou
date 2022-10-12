from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class UserCreateView(APIView):
    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = serializers.UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
