from django.contrib import admin
from django.urls import path,include
from .views import *
# app_name = "main"
urlpatterns = [
    path("a/",doSomething,name="doSomething"),
    path("",listOfFileRoot,name="listoffileroot"),
]
