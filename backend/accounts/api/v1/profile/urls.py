from django.urls import path

from .views import (
    ProfileDestroyView,
    ProfileRetrieveView,
    ProfileUpdateView,
)


urlpatterns = [

    path(
        "",
        ProfileRetrieveView.as_view(),
        name="profile-detail",
    ),

    path(
        "update/",
        ProfileUpdateView.as_view(),
        name="profile-update",
    ),

    path(
        "delete/",
        ProfileDestroyView.as_view(),
        name="profile-delete",
    ),

]