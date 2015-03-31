# Create your views here.
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

from sampleapp.models import Channel, Category, VendorProductDetails, Users, \
    Items


# Serializer for Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','name','email_id','profileimage','phonenumber','secondaryphonenumber','userRole','createdate')


# Serializer for Channel
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel            
        fields = ('id','name','createdate')



# Serializer for Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','description','createdate')


# Serializer for VendorProductDetails
class VendorProductDetailsSerializer(serializers.ModelSerializer):
    userId = UsersSerializer()
    channelId = ChannelSerializer()
    categoryId = CategorySerializer()
    
    class Meta:
        model = VendorProductDetails
        fields = ('id','name','userId','channelId','categoryId','productStatus','productCount','createdate')

# Serializer for VendorProductDetails
class ItemsSerializer(serializers.ModelSerializer):
    vendorProductDetailsId = VendorProductDetailsSerializer()
    class Meta:
        model = Items
        fields = ('id','name','description','vendorProductDetailsId','itemStatus','createdate')



