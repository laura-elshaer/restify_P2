from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import  Comment
from property.models import Property
from .serializers import UserCommentSerializer, PropertyCommentSerializer, CommentSerializer, ReplySerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User


class AddCommentP(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertyCommentSerializer

class GetComments(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset
    
    
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
       
        

class AddComment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCommentSerializer

class Reply(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReplySerializer

