# Create your views here.
import binascii
import datetime
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from rest_framework.parsers import JSONParser

from sampleapp.models import Users, Channel, Category, VendorProductDetails, \
    Items
from sampleapp.serializers import ChannelSerializer, CategorySerializer, \
    VendorProductDetailsSerializer, ItemsSerializer


### Apis for inventory management
def date_handler(obj):
    print obj.isoformat()
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
      

def Login(request):
    if request.method == 'GET':
        print "*******Login Api*******"
        Phonenumber = request.GET.get('phonenumber')
        Password = request.GET.get('password') 
        checkUser = Users.objects.filter(Q(phonenumber = Phonenumber),Q(password = Password))[:1]
        if len(checkUser) > 0:
            userObj = Users.objects.get(id=checkUser[0].id)
            token = binascii.hexlify(os.urandom(10))
            userObj.token = token
            userObj.save()
            return HttpResponse(json.dumps({"Token":token,"status":"True"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message":"Please Contact Sansh team to add you!!!","status":"False"}), content_type="application/json")
            

def GetChannel(request):
    if request.method == 'GET':
        requestMeta = request.META
        if ('HTTP_AUTHTOKEN' not in requestMeta.keys() or 'HTTP_PHONENUMBER' not in requestMeta.keys()):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        elif (requestMeta['HTTP_AUTHTOKEN'] is  None or requestMeta['HTTP_PHONENUMBER'] is  None  ):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        else:
            try:
                CheckUser = Users.objects.get(Q(phonenumber = requestMeta['HTTP_PHONENUMBER']),Q(token = requestMeta['HTTP_AUTHTOKEN']))
                getallCannels = Channel.objects.all()
                serializer = ChannelSerializer(getallCannels,many=True)
                record = {}
                record['status'] = True
                record['data'] = serializer.data
                finalArray = []
                finalArray.append(record)
                return HttpResponse(json.dumps(finalArray,default=date_handler), content_type="application/json")
            except:
                return HttpResponse(json.dumps({"message":"Don't fool us!! only authorized User will get info","status":"False"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message":"Only GET request","status":"False"}), content_type="application/json")



def GetCategory(request):
    if request.method == 'GET':
        requestMeta = request.META
        if ('HTTP_AUTHTOKEN' not in requestMeta.keys() or 'HTTP_PHONENUMBER' not in requestMeta.keys()):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        elif (requestMeta['HTTP_AUTHTOKEN'] is  None or requestMeta['HTTP_PHONENUMBER'] is  None  ):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        else:
            try:
                CheckUser = Users.objects.get(Q(phonenumber = requestMeta['HTTP_PHONENUMBER']),Q(token = requestMeta['HTTP_AUTHTOKEN']))
                getallCannels = Category.objects.all()
                serializer = CategorySerializer(getallCannels,many=True)
                record = {}
                record['status'] = True
                record['data'] = serializer.data
                finalArray = []
                finalArray.append(record)
                return HttpResponse(json.dumps(finalArray,default=date_handler), content_type="application/json")                
            except:
                return HttpResponse(json.dumps({"message":"Don't fool us!! only authorized User will get info","status":"False"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message":"Only GET request","status":"False"}), content_type="application/json")



def GetMyProductDetails(request):
    if request.method == 'GET':
        requestMeta = request.META
        print "Phone Number"
        print requestMeta['HTTP_PHONENUMBER']
        if ('HTTP_AUTHTOKEN' not in requestMeta.keys() or 'HTTP_PHONENUMBER' not in requestMeta.keys()):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        elif (requestMeta['HTTP_AUTHTOKEN'] is  None or requestMeta['HTTP_PHONENUMBER'] is  None  ):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        else:
            try:
                CheckUser = Users.objects.get(Q(phonenumber = requestMeta['HTTP_PHONENUMBER']),Q(token = requestMeta['HTTP_AUTHTOKEN']))
                getallCannels = VendorProductDetails.objects.filter(userId__id = CheckUser.id)
                record = {}
                record['data'] = []
                for aproduct in getallCannels:
                    record1 = {}
                    getaCannels = VendorProductDetails.objects.get(id=aproduct.id)
                    serializer = VendorProductDetailsSerializer(getaCannels)
                    print "serializer"
                    Openitems = Items.objects.filter(vendorProductDetailsId__id = getaCannels.id).filter(itemStatus="1").aggregate(Count('id'))
                    print Openitems  
                    record1['open'] =  Openitems['id__count']  
                    ordereditems = Items.objects.filter(vendorProductDetailsId__id = getaCannels.id).filter(itemStatus="2").aggregate(Count('id'))
                    print ordereditems  
                    record1['ordered'] =  ordereditems['id__count']  
                    Pendingitems = Items.objects.filter(vendorProductDetailsId__id = getaCannels.id).filter(itemStatus="3").aggregate(Count('id'))
                    print ordereditems  
                    record1['Pending'] =  Pendingitems['id__count']  
                    solditems = Items.objects.filter(vendorProductDetailsId__id = getaCannels.id).filter(itemStatus="4").aggregate(Count('id'))
                    print solditems  
                    record1['sold'] =  solditems['id__count']  
                    
                    dest = dict(serializer.data)  # or orig.copy()
                    dest.update(record1)
                        
                    record['data'].append(dest)
                record['status'] = True
                
         #     finalArray = []
          #      finalArray.append(record)
                return HttpResponse(json.dumps(record,default=date_handler), content_type="application/json")                                
            except:
                return HttpResponse(json.dumps({"message":"Don't fool us!! only authorized User will get info","status":"False"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message":"Only GET request","status":"False"}), content_type="application/json")



def GetMyItems(request):
    if request.method == 'GET':
        requestMeta = request.META
        if ('HTTP_AUTHTOKEN' not in requestMeta.keys() or 'HTTP_PHONENUMBER' not in requestMeta.keys()):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        elif (requestMeta['HTTP_AUTHTOKEN'] is  None or requestMeta['HTTP_PHONENUMBER'] is  None  ):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        else:
            try:
                CheckUser = Users.objects.get(Q(phonenumber = requestMeta['HTTP_PHONENUMBER']),Q(token = requestMeta['HTTP_AUTHTOKEN']))
                getallCannels = Items.objects.filter(vendorProductDetailsId__userId__id = CheckUser.id)
                serializer = ItemsSerializer(getallCannels,many=True)
                record = {}
                record['status'] = True
                record['data'] = serializer.data
                finalArray = []
                finalArray.append(record)
                return HttpResponse(json.dumps(finalArray,default=date_handler), content_type="application/json")                                
            except:
                return HttpResponse(json.dumps({"message":"Don't fool us!! only authorized User will get info","status":"False"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message":"Only GET request","status":"False"}), content_type="application/json")



def PostMyProductDetails(request):
    if request.method == 'GET':
        requestMeta = request.META
        if ('HTTP_AUTHTOKEN' not in requestMeta.keys() or 'HTTP_PHONENUMBER' not in requestMeta.keys()):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        elif (requestMeta['HTTP_AUTHTOKEN'] is  None or requestMeta['HTTP_PHONENUMBER'] is  None  ):
            return HttpResponse(json.dumps({"status": "UNAUTHORIZED"}), content_type="application/json")
        else:
            try:
                CheckUser = Users.objects.get(Q(phonenumber = requestMeta['HTTP_PHONENUMBER']),Q(token = requestMeta['HTTP_AUTHTOKEN']))
                data = JSONParser().parse(request)
                getCannel = VendorProductDetails.objects.filter(Q(name=data['name']),Q(userId__id = CheckUser.id),Q(channelId__id = data['cannelId']),Q(categoryId__id = data['categoryId']))
                if len(getCannel) > 0:
                    return HttpResponse(json.dumps({"message":"This product is already added","status":"False"}), content_type="application/json")
                else:
                    VendorProductDetailsObj = VendorProductDetails()
                    VendorProductDetailsObj.categoryId = Category.objects.get(id = data['cannelId'])
                    VendorProductDetailsObj.channelId = Channel.objects.get(id = data['cannelId'])
                    VendorProductDetailsObj.userId = Users.objects.get(id = CheckUser.id)
                    VendorProductDetailsObj.createdate = datetime.datetime.now()
                    VendorProductDetailsObj.name = data['name']                    
                    if 'description' in data:
                        VendorProductDetailsObj.description = data['description']
                    VendorProductDetailsObj.save()
                    return HttpResponse(json.dumps({"message":"Updated","status":"True"}), content_type="application/json")                                
            except:
                return HttpResponse(json.dumps({"message":"Don't fool us!! only authorized User will get info","status":"False"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message":"Only GET request","status":"False"}), content_type="application/json")






