from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ProductSerializer
from .models import Product
from rest_framework.decorators import action
from .serializers import ProductSerializer
from .models import Product
from rest_framework.viewsets import ReadOnlyModelViewSet

from .utils import EXPAND_PARAM,is_expanded
from .models import Image
from .serializers import ImageSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
# Create your views here.

class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permit_list_expands = ['category', 'sites', 'comments', 'sites.company', 'sites.productsize']

    def get_queryset(self):
        queryset = Product.objects.all()

        if is_expanded(self.request, 'category'):
            queryset = queryset.prefetch_related('category')

        if is_expanded(self.request, 'comments'):
            queryset = queryset.prefetch_related('comments')

        if is_expanded(self.request, 'sites'):
            queryset = queryset.prefetch_related('sites')

        if is_expanded(self.request, 'company'):
            queryset = queryset.prefetch_related('sites__company')

        if is_expanded(self.request, 'productsize'):
            queryset = queryset.prefetch_related('sites__productsize')

        return queryset
    
    @action(detail=False)
    def get_list(self, request):
        pass
      
    @action(detail=True)
    def get_product(self, request, pk=None):
        pass


    @action(detail=True, methods=['post', 'delete'])
    def delete_product(self, request, pk=None):
        pass

class ImageViewSet(FlexFieldsModelViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()