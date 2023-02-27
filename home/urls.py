from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('contactus/',contactus,name='contactus'),
    path('contactpage/',contactpage,name='contactpage'),
    path('news/',news,name='news'),
    path('services/',services,name='services'),
    path('gallery/',gallery,name='gallery'),
    path('emicalculator/',emicalculator,name='emicalculator'),
    path('getcontact/',getcontact,name='getcontact'),
    path('galleryview/<str:id>',galleryview,name='galleryview'),
    path('newsingle/<str:id>',newsingle,name='newsingle'),
    path('admin/',adminlogin,name='adminlogin'),
    path('adminlogout/',adminlogout,name='adminlogout'),
    path('adminhome/',adminhome,name='adminhome'),
    path('admingallery/',admingallery,name='admingallery'),
    path('adminviewgallery/',adminviewgallery,name='adminviewgallery'),
    path('admingalleryimageadd/',admingalleryimageadd,name='admingalleryimageadd'),
    path('adminnews/',adminnews,name='adminnews'),
    path('adminnewsview/',adminnewsview,name='adminnewsview'),
    path('adminadd/',adminadd,name='adminadd'),
    path('admincontactview/',admincontactview,name='admincontactview'),
    path('admingalleryimage/<str:id>/',admingalleryimage,name='admingalleryimage'),
    path('contactviewsingle/<str:id>/',contactviewsingle,name='contactviewsingle'),
]
