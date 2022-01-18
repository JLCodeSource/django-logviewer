from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from logviewer import views

router = DefaultRouter()
router.register(r"assets", views.AssetViewSet)
router.register(r"logs", views.LogViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
