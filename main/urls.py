from django.contrib import admin
from django.urls import path,include
from .views import *
# app_name = "main"
urlpatterns = [
    path("a/",doSomething,name="doSomething"),
    # path("w/<str:thePath>",editFile,name="editfile"),
    path("e/",listOfFile,name="listoffile"),
    path("",listOfFileRoot,name="listoffileroot"),
]
