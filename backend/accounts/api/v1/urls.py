from django.urls import include, path


urlpatterns = [

    path(
        "auth/",
        include("accounts.api.v1.auth.urls"),
    ),
    path(
        "user/",
        include("accounts.api.v1.user.urls"),
    ),
    path(
        "profile/",
        include("accounts.api.v1.profile.urls"),
    ),
]