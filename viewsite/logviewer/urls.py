from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from logviewer import views

urlpatterns = [
    path("", views.index, name="index"),
    path("assets/", views.AssetList.as_view()),
    path("assets/<int:pk>/", views.AssetDetail.as_view()),
    path("logs/", views.LogList.as_view()),
    path("logs/<int:pk>/", views.LogDetail.as_view()),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
