from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from logviewer.models import Asset, Log
from logviewer.serializers import AssetSerializer, LogSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello, World")


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "assets": reverse("asset-list", request=request, format=format),
            "logs": reverse("log-list", request=request, format=format),
        }
    )


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
