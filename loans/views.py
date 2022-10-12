from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class UserCreateView(APIView):
    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user = models.User.objects.with_totals().get(pk=user.id)
        serializer = serializers.UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoanCreateView(APIView):
    def post(self, request):
        serializer = serializers.LoanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loan = serializer.save()

        return Response(request.data, status=status.HTTP_201_CREATED)


class UserListView(APIView):
    def get(self, request):
        users = models.User.objects.with_totals()
        serializer = serializers.UserSerializer(users, many=True)

        return Response(serializer.data)
