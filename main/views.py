from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .theTreeBase import *
import sys, shutil, os, imghdr, pickle


theFileExplorerObject = FileSystem(10000000000)

theRootPathOfFiles = "theFileExplorerBase/"
theFirstCurrentPath = "This PC"
try :
    os.listdir(theRootPathOfFiles)
except :
    os.mkdir(theRootPathOfFiles)

thePickleFile = "theFileExplorerBase.pickle"
def savePickle() :
    global thePickleFile, theFileExplorerObject
    with open(thePickleFile, 'wb') as handle:
        pickle.dump(theFileExplorerObject, handle, protocol=pickle.HIGHEST_PROTOCOL)
def loadPickle() :
    global thePickleFile
    with open(thePickleFile, 'rb') as handle:
        loadedDictVar = pickle.load(handle)
        return loadedDictVar


if(not os.path.exists(thePickleFile)) :
    savePickle(FileSystem(10000000))
theFileExplorerObject = loadPickle()

def calCurrentPath() :
    theDict = {}
    print(theFileExplorerObject.pwd(),"****************************")
    currentPath = theFileExplorerObject.pwd().split("/")
    print(currentPath,"-+-+--+-++-+-")
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
def listOfFileRoot(r) :
    print(theFileExplorerObject.get_children_dict())
    theAllFile = theFileExplorerObject.get_children_dict()
    # print(theAllFile)
    theResult = {}
    for d in theAllFile :
        # theResult[d] = {"type":"drive","forO":d,"href":reverse("listoffile",args=[d])}
        theResult[d] = {"type":"drive","forO":d,"href":f"theJsFunctionCd('{d}')"}
    print(calCurrentPath())
    # return render(r,"showFolder2.html",{"tehCurentPath":calCurrentPath(),"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":"","fileTree":getAllDir(r)})
    return render(r,"showFolder2.html",{"tehCurentPath":calCurrentPath(),"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":"","fileTree":""})
def listOfFile(r) :
    pass
    # thePath = makePathUsable(thePath)
    # theAllFile = getListOfFileFromFolderPath(thePath)
    # # print(theAllFile)
    # theResult = getPathOfTheAllFile(thePath)
    # currentPath = calCurrentPath(thePath)
    # # print(currentPath)
    # # print(theResult)
    
    # # return render(r,"showFolder2.html",{"tehCurentPath":currentPath,"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":thePath.replace(theRootPathOfFiles,""),"fileTree":getAllDir(r)})
    # return render(r,"showFolder2.html",{"tehCurentPath":currentPath,"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":thePath.replace(theRootPathOfFiles,""),"fileTree":""})


@csrf_exempt
def doSomething(r) :

    if r.method == "POST" :
        print("------------------------------------------------------------")
        data = r.POST
        print(data)
        if data['mode'] == "newFolder" :
            print("OKokokok")
            theNewFolder = DirNode(data['new'])
            print(theFileExplorerObject.add_dir(theNewFolder))
            savePickle()
        if data['mode'] == "cd" :
            theCdDir = DirNode(data['cd'])
            print("=>",theCdDir)
            print(theFileExplorerObject.cd(theCdDir))
        print("------------------------------------------------------------")


        return JsonResponse({"CODE":200})
    return JsonResponse({"CODE":400})



"""def getfileContent(path) :
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
def getAllDir(r) :
    theResult = []
    for dirname, dirnames, filenames in os.walk(theRootPathOfFiles):
        for subdirname in dirnames:
            theResult.append(os.path.join(dirname, subdirname).replace("\\","/").replace(theRootPathOfFiles,""))
    fileTree = {}
    for path in theResult:
        parts = path.split('/')
        node = fileTree
        for part in parts:
            node = node.setdefault(f"{part}", {})
    print(fileTree)
    return fileTree
# {{ name|split:':_:_:'|getItem:1 }}
def listOfFileRoot(r) :
    
    theAllFile = getListOfFileFromFolderPath(theRootPathOfFiles)
    # print(theAllFile)
    theResult = {}
    for d in theAllFile :
        theResult[d] = {"type":"drive","forO":d,"href":reverse("listoffile",args=[d])}
    print(calCurrentPath(theRootPathOfFiles))
    return render(r,"showFolder2.html",{"tehCurentPath":calCurrentPath(theRootPathOfFiles),"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":"","fileTree":getAllDir(r)})
def listOfFile(r,thePath) :
    thePath = makePathUsable(thePath)
    theAllFile = getListOfFileFromFolderPath(thePath)
    # print(theAllFile)
    theResult = getPathOfTheAllFile(thePath)
    currentPath = calCurrentPath(thePath)
    # print(currentPath)
    # print(theResult)
    
    return render(r,"showFolder2.html",{"tehCurentPath":currentPath,"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":thePath.replace(theRootPathOfFiles,""),"fileTree":getAllDir(r)})
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
    return JsonResponse({"CODE":400})"""