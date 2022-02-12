from rest_framework import serializers
from .models import Company,Category,ProductSize,CustomerReportRecord,Product ,Comment,ProductSite,Image
from django.utils.timezone import now
from django.contrib.auth.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer


#----------------------------------------------------
#Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'name', 'url']

#Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']
        expandable_fields = {
          'products': ('reviews.ProductSerializer', {'many': True})
        }

#ProductSize
class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['pk', 'name']

#Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'content', 'created', 'updated']
        expandable_fields = {
            'category': ('MongoApp.CategorySerializer', {'many': True}),
            'sites': ('MongoApp.ProductSiteSerializer', {'many': True}),
            'comments': ('revMongoAppiews.CommentSerializer', {'many': True}),
            'image': ('reviMongoAppews.ImageSerializer', {'many': True}),
        }

#ProductSite
class ProductSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSite
        fields = ['pk', 'name', 'price', 'url', 'created', 'updated']
        expandable_fields = {
            'product': 'MongoApp.CategorySerializer',
            'productsize': 'MongoApp.ProductSizeSerializer',
            'company': 'MongoApp.CompanySerializer',
        }


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username']

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'title', 'content', 'created', 'updated']
        expandable_fields = {
            'product': 'MongoApp.CategorySerializer',
            'user': 'MongoApp.UserSerializer'
        }
 
#----------------------
class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReportRecord        

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['pk', 'name', 'category']





class ImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']      



#-----------------------------------------------------------------
def validate_title(self, value):
    if 'django' not in value.lower():
        raise serializers.ValidationError("hata mesaj")
    
    return value

def validate(self, data):
    if data['start'] > data['finish']:
        raise serializers.ValidationError("Start-...-Finish")
    return data

def create(self, validated_data):
    return Comment.objects.create(**validated_data)

def update(self, instance, validated_data):
    instance.email = validated_data.get('email', instance.email)
    instance.title = validated_data.get('content', instance.title)
    instance.save()
    return instance

