from drf_spectacular.utils import extend_schema

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterResponseSerializer,
    RegisterSerializer,
)


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        self.user = serializer.save()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_create(
            serializer,
        )

        refresh = RefreshToken.for_user(
            self.user,
        )

        response_data = {
            "user": self.user,
            "access": str(
                refresh.access_token
            ),
            "refresh": str(refresh),
        }

        return Response(
            RegisterResponseSerializer(
                response_data,
            ).data,
            status=201,
        )