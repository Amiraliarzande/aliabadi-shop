from django.urls import include, path


urlpatterns = [

    path(
        "auth/",
        include("accounts.api.v1.auth.urls"),
    ),
]