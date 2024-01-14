from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import sys, shutil, os, imghdr

theRootPathOfFiles = "theFileExplorerBase/"
theFirstCurrentPath = "This PC"
try :
    os.listdir(theRootPathOfFiles)
except :
    os.mkdir(theRootPathOfFiles)


def isImage(file_path):
    image_types = imghdr.what(file_path)
    if image_types != None:
        return True
    return False
def getfileContent(path) :
    fullLine = ""
    with open(path, 'r') as file:
        for line in file:
            fullLine += f"{line}"
    return fullLine
def getListOfFileFromFolderPath(folderPath) :
    return os.listdir(folderPath)
def makeDirInPath(thePath,dirName) :
    try :
        os.mkdir(f"{thePath}{dirName}")
        return True
    except :
        return False
def calCurrentPath(thePath) :
    theDict = {}
    currentPath = thePath.split("/")
    currentPath[0] = theFirstCurrentPath
    theBackPath = ""
    for cp in currentPath :
        if cp :
            if cp == theFirstCurrentPath :
                theDict[cp] = {"href":reverse("listoffileroot")}
            else :
                theBackPath += f",{cp}"
                theDict[cp] = {"href":reverse("listoffile",args=[theBackPath.replace(",","",1)])}
    return theDict
def getTypeOfPath(path) :
    theType = "folder"
    if os.path.isfile(path) :
        theType = "rawFile"
    return theType
def makePathUsable(thePath) : 
    thePath = thePath.replace(",","/")
    thePath = f"{theRootPathOfFiles}{thePath}"
    return thePath
def getPathOfTheAllFile(path) :
    theAllFile = getListOfFileFromFolderPath(path)
    theResult = {}
    realPath = path.replace(theRootPathOfFiles,"")
    for d in theAllFile :
        if d != theFirstCurrentPath :
            calTheFForT = getTypeOfPath(f"{path}/{d}")
            forOString = f"{realPath}/{d}".replace("/",",")
            if calTheFForT == "folder" :
                theResult[d] = {"type":"folder","forO":forOString,"href":reverse("listoffile",args=[forOString])}
            elif calTheFForT == "rawFile" :
                theResult[d] = {"type":"rawFile","forO":forOString,"href":reverse("editfile",args=[forOString])}
    return theResult

def listOfFileRoot(r) :
    theAllFile = getListOfFileFromFolderPath(theRootPathOfFiles)
    # print(theAllFile)
    theResult = {}
    for d in theAllFile :
        theResult[d] = {"type":"drive","forO":d,"href":reverse("listoffile",args=[d])}
    print(calCurrentPath(theRootPathOfFiles))
    return render(r,"showFolder2.html",{"tehCurentPath":calCurrentPath(theRootPathOfFiles),"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":""})
def listOfFile(r,thePath) :
    thePath = makePathUsable(thePath)
    theAllFile = getListOfFileFromFolderPath(thePath)
    # print(theAllFile)
    theResult = getPathOfTheAllFile(thePath)
    currentPath = calCurrentPath(thePath)
    # print(currentPath)
    # print(theResult)
    return render(r,"showFolder2.html",{"tehCurentPath":currentPath,"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":thePath.replace(theRootPathOfFiles,"")})
def editFile(r,thePath) :
    thePath = makePathUsable(thePath)
    # print(os.path.realpath(thePath))
    # print(getfileContent(thePath))
    theBackUrl = os.path.dirname(thePath)
    theBackUrl = theBackUrl.replace(theRootPathOfFiles,"").replace("/",",")
    theBackUrl = r.build_absolute_uri(reverse("listoffile",args=[theBackUrl]))
    pathFT = thePath.replace(theRootPathOfFiles,"")
    return render(r,"editFile.html",{"fileContent":getfileContent(thePath),"title":pathFT,"sf":r.build_absolute_uri(reverse("doSomething")),"backUrl":theBackUrl})
@csrf_exempt
def doSomething(r) :

    if r.method == "POST" :
        data = r.POST
        if data['mode'] == "save" :
            theC = data['content'].strip()
            # print(theC)
            path = f"{theRootPathOfFiles}{data['path']}"
            # print(path)
            with open(path, 'w') as file:
                file.write(theC)
                file.close()
        if data['mode'] == "rename" :
            thePath = makePathUsable(data['key'])
            head, tail = os.path.split(thePath)
            newName = data['to']
            newPath = os.path.join(head, newName).replace("\\","/")
            # print(thePath,newPath)
            os.rename(thePath, newPath)
        if data['mode'] == "delete" :
            thePath = makePathUsable(data['key'])
            try :
                shutil.rmtree(thePath)
            except :
                os.remove(thePath)
        if data['mode'] == "newFolder" :
            thePath = makePathUsable(data['key'])
            print(thePath)
            os.mkdir(f"{thePath}/{data['new']}")
        if data['mode'] == "newFile" :
            thePath = makePathUsable(data['key'])
            file = open(f"{thePath}/{data['new']}", 'w')
            file.close()
            # os.mkdir(f"{thePath}/{data['new']}")


        return JsonResponse({"CODE":200})
    return JsonResponse({"CODE":400})