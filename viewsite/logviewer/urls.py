from django.urls import path

from logviewer import views

urlpatterns = [
    path("", views.index, name="index"),
    path("assets/", views.asset_list),
    path("assets/<int:pk>/", views.asset_detail),
]
