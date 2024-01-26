from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .theTreeBase import *
import sys, shutil, os, imghdr, pickle


theFileExplorerObject = FileSystem(10000000000)
 

theRootPathOfFiles = "theFileExplorerBase/"
theFirstCurrentPath = "This PC"

# try :
#     os.listdir(theRootPathOfFiles)
# except :
#     os.mkdir(theRootPathOfFiles)

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
    savePickle()
    theFileExplorerObject = loadPickle()
    theFileExplorerObject.theFirstRun = True
else :
    theFileExplorerObject = loadPickle()
"""if(not os.path.exists(thePickleFile)) :
    savePickle()
theFileExplorerObject = loadPickle()"""

def getAllDir() :
    theCopyOfEx = deepcopy(theFileExplorerObject)
    theCopyOfEx.reset_up_arrow()
    fileTree = {}
    print(theCopyOfEx.getAllDirectoryPaths(),"= "*20)
    for path in theCopyOfEx.getAllDirectoryPaths() :
        parts = path.split('/')
        node = fileTree
        for part in parts:
            node = node.setdefault(f"{part}", {})
    print(fileTree)
    return fileTree

def calCurrentPath() :
    theDict = {}
    # print(theFileExplorerObject.pwd(),"****************************")
    currentPath = theFileExplorerObject.pwd()
    print("- "*10,currentPath)
    currentPath[0] = theFirstCurrentPath
    theBackPath = ""
    for cp in currentPath :
        if cp :
            if cp == theFirstCurrentPath :
                theDict[cp] = {"href":reverse("listoffileroot")}
            else :
                theBackPath += f",{cp}"
                # theDict[cp] = {"href":reverse("listoffile",args=[theBackPath.replace(",","",1)])}
                theDict[cp] = {"href":""}
    return theDict
def listOfFileRoot(r) :
    global theFileExplorerObject
    if(theFileExplorerObject.inEditMode == True) :
        return render(r,"editFile.html",{"fileContent":"CONTECNT","title":"THE PATH","sf":r.build_absolute_uri(reverse("doSomething")),"backUrl":"doBackUrl()"})
        

    # print(theFileExplorerObject.get_children_dict())
    theAllFile = theFileExplorerObject.get_children_dict()
    # print(theAllFile)
    theResult = {}
    print(theAllFile)
    # weInRoot = theFileExplorerObject.inRoot()
    theCP = calCurrentPath()
    showNewFile = True
    theNameNewFolder = "folder"
    if len(theCP) == 1 :
        showNewFile = False
        theNameNewFolder = "drive"
        
    for d in theAllFile :
        # theResult[d] = {"type":"drive","forO":d,"href":reverse("listoffile",args=[d])}
        tmpTyp = theAllFile[d]
        theJsFunc = f"theJsFunctionCd('{d}')"
        if tmpTyp == "directory" :
            tmpTyp = "folder"
            if len(theCP) == 1 :
                tmpTyp = "drive"
        else :
            tmpTyp = "rawFile"
            theJsFunc = f"theJsFunctionOpen('{d}')"
        theResult[d] = {"type":tmpTyp,"forO":d,"href":theJsFunc}
    # print(calCurrentPath())
    # return render(r,"showFolder2.html",{"tehCurentPath":calCurrentPath(),"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":"","fileTree":getAllDir(r)})
    # getAllDir()
    print("=> "*10,theFileExplorerObject.theFirstRun)
    return render(r,"showFolder2.html",{"tehCurentPath":theCP,"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":"","fileTree":getAllDir(),"showNewFile":showNewFile,"theNameNewFolder":theNameNewFolder,"isInCutOrCopy":theFileExplorerObject.isInCutOrCopy,"theFirstRun":theFileExplorerObject.theFirstRun})


@csrf_exempt
def doSomething(r) :
    global theFileExplorerObject
    if r.method == "POST" :
        print("------------------------------------------------------------")
        data = r.POST
        print(data)
        if data['mode'] == "firstRun" :
            print("firstRun........... size = ",data['size'])
            theFileExplorerObject = FileSystem(int(data['size']))
            savePickle()
        if data['mode'] == "newFolder" :
            print(theFileExplorerObject.mkdir(data['new']))
        elif data["mode"] == "newDrive" :
            print(theFileExplorerObject.mkdrive(data['new'],int(data['size'])))
        elif data['mode'] == "newFile" :
            print(theFileExplorerObject.mkfile(data['new'],"txt"))
        elif data['mode'] == "cd" :
            print("=>",data['cd'])
            print(theFileExplorerObject.cd_name(data['cd']))
        elif data["mode"] == "back" :
            print(theFileExplorerObject.go_backward_arrow())
        elif data["mode"] == "forward" :
            print(theFileExplorerObject.go_forward_arrow())
        elif data["mode"] == "up" :
            print(theFileExplorerObject.reset_up_arrow())
        elif data["mode"] == "open" :
            theFileExplorerObject.inEditMode = True
        elif data["mode"] == "close" :
            theFileExplorerObject.inEditMode = False
        elif data["mode"] == "delete" :
            theFileExplorerObject.delete_name(data['key'])
            print("dd",data)
        elif data["mode"] == "rename" :
            theFileExplorerObject.rename(data["key"],data["to"])
        elif data["mode"] == "copy" :
            theFileExplorerObject.isInCutOrCopy = True
            theFileExplorerObject.copy_name(data["key"])
        elif data["mode"] == "cut" :
            theFileExplorerObject.isInCutOrCopy = True
            theFileExplorerObject.cut_name(data["key"])
        elif data["mode"] == "paste" :
            theFileExplorerObject.isInCutOrCopy = False
            theFileExplorerObject.paste()
        elif data["mode"] == "cancelCC" :
            theFileExplorerObject.isInCutOrCopy = False
        print("------------------------------------------------------------")

        savePickle()
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