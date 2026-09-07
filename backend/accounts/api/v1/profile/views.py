from drf_spectacular.utils import extend_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ProfileDeleteSerializer,
    ProfilePartialUpdateSerializer,
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
)


class ProfileRetrieveView(
    generics.RetrieveAPIView
):

    serializer_class = ProfileRetrieveSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(
    generics.UpdateAPIView
):

    serializer_class = ProfileUpdateSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.profile



class ProfileDestroyView(
    generics.DestroyAPIView
):

    serializer_class = ProfileDeleteSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.profile