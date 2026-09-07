from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

from .serializers import (
    UserDeleteSerializer,
    UserListSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)


class UserListView(generics.ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserListSerializer

    permission_classes = [
        IsAuthenticated,
    ]


class UserRetrieveView(generics.RetrieveAPIView):

    queryset = User.objects.all()

    serializer_class = UserRetrieveSerializer

    permission_classes = [
        IsAuthenticated,
    ]

class UserUpdateView(generics.UpdateAPIView):

    queryset = User.objects.all()

    serializer_class = UserUpdateSerializer

    permission_classes = [
        IsAuthenticated,
    ]


class UserDestroyView(generics.DestroyAPIView):

    queryset = User.objects.all()

    serializer_class = UserDeleteSerializer

    permission_classes = [
        IsAuthenticated,
    ]