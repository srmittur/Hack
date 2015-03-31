# Create your views here.

from django.contrib import admin

from sampleapp.models import Users, Channel, Category, VendorProductDetails, \
    Items


class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_id', 'phonenumber','userRole','createdate')
    list_filter = ('userRole',)
    
admin.site.register(Users,UsersAdmin) 

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'createdate')
    list_filter = ('name',)
    
admin.site.register(Channel,ChannelAdmin) 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','createdate')
    list_filter = ('name',)
    
admin.site.register(Category,CategoryAdmin) 

class VendorProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'userId','channelId','categoryId','productStatus','createdate')
    list_filter = ('channelId','categoryId','productStatus')
    
admin.site.register(VendorProductDetails,VendorProductDetailsAdmin) 


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'vendorProductDetailsId','itemStatus','createdate')
    list_filter = ('itemStatus',)
    
admin.site.register(Items,ItemsAdmin) 
