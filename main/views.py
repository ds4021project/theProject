from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .theTreeBase import *
import sys, shutil, os, imghdr, pickle


theFileExplorerObject = FileSystem(10000000000)
 

theFirstCurrentPath = "This PC"

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
                theDict[cp] = {"href":""}
    return theDict
def listOfFileRoot(r) :
    global theFileExplorerObject
    theAllFile = theFileExplorerObject.get_children_dict()
    theResult = {}
    print(theAllFile)
    theCP = calCurrentPath()
    showNewFile = True
    theNameNewFolder = "folder"
    if len(theCP) == 1 :
        showNewFile = False
        theNameNewFolder = "drive"
        
    for d in theAllFile :
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
    print("=> "*10,theFileExplorerObject.theFirstRun)
    return render(r,"showExplorer.html",{"tehCurentPath":theCP,"listOfFiles":theResult,"apil":r.build_absolute_uri(reverse("doSomething")),"currentPathForNew":"","fileTree":getAllDir(),"showNewFile":showNewFile,"theNameNewFolder":theNameNewFolder,"isInCutOrCopy":theFileExplorerObject.isInCutOrCopy,"theFirstRun":theFileExplorerObject.theFirstRun})


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
            result = theFileExplorerObject.mkdrive(data['new'],int(data['size']))
            print(result)
            if result == False :
                return HttpResponseBadRequest("bad")
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
    return HttpResponseBadRequest("bad")