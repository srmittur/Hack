from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.messages.api import success

from sampleapp.views import Login, GetMyProductDetails, GetChannel, GetCategory, \
    GetMyItems, PostMyProductDetails


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
       
     #login and authentication     
     url(r'^login/?$',Login),
     url(r'^getMyProducts/?$',GetMyProductDetails),
     url(r'^getallChannel/?$',GetChannel),
     url(r'^getallCategory/?$',GetCategory),
     url(r'^getMyItem/?$',GetMyItems),
     url(r'^postMyProducts/?$',PostMyProductDetails),
     
             
)