from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework_bulk import BulkModelViewSet
from logviewer.models import Asset, Log
from logviewer.serializers import AssetSerializer, LogSerializer


class AssetViewSet(BulkModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class LogViewSet(BulkModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
