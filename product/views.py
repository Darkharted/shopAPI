# from model_utils import fields
# import product
# from django import http
# from django.shortcuts import render
# from rest_framework import relations, serializers
# from rest_framework import views
# from rest_framework.views import APIView
# from .models import CreateDateModel, Product, ProductReview
# from .serializers import ProductListSerializer, ProductDetailSerializer, \
#     ProductCreateSerializer, ProductReviewSerializer
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, \
#     UpdateAPIView, DestroyAPIView, CreateAPIView
# from rest_framework import viewsets

import product
from .models import Product, ProductReview
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer, ProductReviewSerializer
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, \
    UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import permissions

from product import serializers




# 127.0.0.1:8000/products/
# 1. Подход с созданием функции 
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializers(products, many=True)
#     return Response(serializers.data)

# 2. Создание класса от APIView
# class ProductListView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializers = ProductSerializers(products, many=True)
#         return Response(serializers.data)
    
#     def delete(self,request):

    
#     def update():
    # ...

# 3. GenericAPIView(
#     CRUD
    # CRUD -> POST, GET, PATH, PUT 
    # Create -> POST 
    # Read -> GET
    # Update -> PATCH, PUT 
    # Delete -> DELETE
# )

# class ProductListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class =  ProductListSerializer

# #RetrieveAPIView -> Отвечает за получение конкретной данные
# class ProductDetailView(RetrieveAPIView):
#     """
#     GET метод
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer


# class ProductDetailView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# Read -> Create, Update, Delete

# class ProductUpdateView(UpdateAPIView):
#     """
#     PUT, PATCH метод
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductCreateSerializer


# class ProductDeleteView(DestroyAPIView):
#     """
#     DELETE метод
#     """
#     queryset = Product.objects.all()
#     serializers_class = ProductListSerializer


# class ProductCreateView(CreateAPIView):
#     """
#     POST метод 
#     """
#     queryset = Product.objects.all()
#     serializers_class = ProductCreateSerializer


# 4. ModelViewSet(
#   CreateMixin, UpdateMixin, DeleteMixin, RetrieveMixin
# )

class ProductReviewViewset(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {
            'request': self.request
        }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends =  [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['price', 'title']
    search_fields = ['title', 'description']
    permissions_classes = [permissions.IsAdminUser()]


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAdminUser()]
        return []


    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'delete':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductCreateSerializer
    
    @action(['GET'], detail=True)
    def reviews(self,request,pk=None):
        product = self.get_object()
        reviews = ProductReview.objects.filter(product=product)
        reviews = product.reviews.all()
        serializer = ProductReviewSerializer(
            reviews, many=True
        ).data
        return Response(serializer, status=200)