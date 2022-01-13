from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from logviewer import views

asset_list = views.AssetViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

asset_detail = views.AssetViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

log_list = views.LogViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

log_detail = views.LogViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


urlpatterns = [
    path("", views.index, name="index"),
    path("assets/", asset_list, name="asset-list"),
    path("assets/<int:pk>/", asset_detail, name="asset-detail"),
    path("logs/", log_list, name="log-list"),
    path("logs/<int:pk>/", log_detail, name="log-detail"),
    path("api-auth/", include("rest_framework.urls")),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
