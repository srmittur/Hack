from django.db import models

# Create your models here.


class Users(models.Model):
    Status = (
    ('1', 'Admin'),
    ('2', 'ChannelAdmin')
    
    ) 
    name = models.CharField(max_length=256,verbose_name="Name")
    password = models.CharField(max_length=256,verbose_name="Password")
    email_id = models.CharField(max_length=256,verbose_name="Email Id") 
    profileimage = models.ImageField(upload_to = "sampleapp/static/images",null=True, blank=True)  
    token = models.CharField(max_length=20,verbose_name="Auth Token")      
    phonenumber = models.CharField(max_length=20, verbose_name="Phone Number",unique=True) 
    secondaryphonenumber = models.CharField(max_length=20, verbose_name="Secondary Phone Number",null=True, blank=True) 
    userRole = models.CharField(max_length=20,choices=Status,verbose_name="User Role",null=True,blank=True)
    createdate = models.DateTimeField(verbose_name='created At',null=True, blank=True)
    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "Users"
        db_table = "User"
    def __unicode__(self):
        return  str(self.phonenumber) 

class Channel(models.Model):
    name = models.CharField(max_length=256,verbose_name="Channel Name")
    createdate = models.DateTimeField(verbose_name='created At',null=True, blank=True)
    class Meta:
        verbose_name_plural = "Channel"
        verbose_name = "Channel"
        db_table = "Channel"
    def __unicode__(self):
        return  str(self.name) 
    

 
    
class Category(models.Model):
    name = models.CharField(max_length=256,verbose_name="Category Name")
    description = models.TextField(verbose_name="Description",null=True, blank=True)  
    createdate = models.DateTimeField(verbose_name='created At',null=True, blank=True)
    class Meta:
        verbose_name_plural = "Category"
        verbose_name = "Category"
        db_table = "Category"
    def __unicode__(self):
        return  str(self.name)
   
class VendorProductDetails(models.Model):
    Status = (
    ('1', 'Open'),
    ('2', 'less Stock'),
    ('3', 'Sold')    
    ) 
    
    name = models.CharField(max_length=256,verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description",null=True, blank=True)
    userId = models.ForeignKey(Users)
    channelId = models.ForeignKey(Channel)
    categoryId = models.ForeignKey(Category)  
    productStatus = models.CharField(max_length=20,choices=Status,verbose_name="Product Status") 
    productCount = models.IntegerField(verbose_name='Product Count')
    createdate = models.DateTimeField(verbose_name='created At',null=True, blank=True)
    class Meta:
        verbose_name_plural = "Vendor Product Details"
        verbose_name = "Vendor Product Details"
        db_table = "VendorProductDetails"
    def __unicode__(self):
        return  str(self.name)



class Items(models.Model):
    Status = (
    ('1', 'Open'),
    ('2', 'Ordered'),
    ('3', 'Pending'),
    ('4', 'Sold'),  
    )     
    name = models.CharField(max_length=256,verbose_name="Item Name")
    description = models.TextField(verbose_name="Product Description",null=True, blank=True)
    vendorProductDetailsId = models.ForeignKey(VendorProductDetails)
    itemStatus = models.CharField(max_length=20,choices=Status,verbose_name="Item Status")
    itemCount = models.IntegerField(verbose_name='Item Count')
    createdate = models.DateTimeField(verbose_name='created At',null=True, blank=True)    
    class Meta:
        verbose_name_plural = "Items"
        verbose_name = "Items"
        db_table = "Items"
    def __unicode__(self):
        return  str(self.name)
    
        
    
    
    
    

 

    
    
