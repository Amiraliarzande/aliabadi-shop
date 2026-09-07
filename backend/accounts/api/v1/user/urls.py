from django.urls import path

from .views import (
    UserDestroyView,
    UserListView,
    UserRetrieveView,
    UserUpdateView,
)


urlpatterns = [

    path(
        "",
        UserListView.as_view(),
        name="user-list",
    ),

    path(
        "<int:pk>/",
        UserRetrieveView.as_view(),
        name="user-detail",
    ),

    path(
        "<int:pk>/update/",
        UserUpdateView.as_view(),
        name="user-update",
    ),

    path(
        "<int:pk>/delete/",
        UserDestroyView.as_view(),
        name="user-delete",
    ),

]