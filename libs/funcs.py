#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import shutil, errno
import os
import ConfigParser
import hashlib
import difflib

#
#varialble
#
diffC = difflib.Differ()

if os.name == "posix":
    pathSep = "/"
elif os.name == "nt":
    pathSep = "\\"
else:
    print "can not detect OS!"
    exit(2)
#
#functions
#  


def createProject(pName, sDir, version = 1):
    try:
        if os.path.exists('projects/' + pName):
            print "Project name exists!: " + pName
            sys.exit(1)
        config = ConfigParser.RawConfigParser()
        #copy source
        print "Copying..............................."
        shutil.copytree(sDir,'projects' + pathSep + pName, symlinks=False, ignore=None)
        #create directory for udetect
        print "Finishing............................."
        if not os.path.exists('projects' + pathSep + pName + pathSep + '.udetect'):
            os.makedirs('projects' + pathSep + pName + pathSep + '.udetect')
        #create file config
        config.add_section(pName)
        config.add_section("files")
        config.add_section("directories")        
        config.set(pName, 'pathS', os.path.abspath(sDir))
        config.set(pName, 'version', version)
        config.set("files", 'listS', walkDir(sDir))
        config.set("files", 'listP', walkDir('projects' + pathSep + pName))
        with open('projects'+ pathSep + pName + pathSep + '.udetect'+ pathSep +'.config', 'wb') as configfile:
            config.write(configfile)
        if(version == 1):
            print "Create a project successful: " + pName
    except:
        delProject(pName)

def check(pName, option = "diff"):
    diffCount = 0 
    print "Project Name:\t\t" + pName
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.config'))
    srcDir = config.get(pName,'pathS')
    print "Path:        \t\t" + srcDir
    print
    lstOrg = eval(config.get('files','listS'))
    for i in lstOrg:
        print i[0]
#    raw_input()
    for path, dirs, files in os.walk(srcDir):
        print path

    for i in lstOrg:
        fileTmp = i[0] + pathSep + i[1][0]
        if os.path.exists(fileTmp):
            if not (md5Checksum(fileTmp) == i[1][1]):
                # create a list of lines in text1
                fileOrg =  fileTmp.replace(srcDir,"projects" + pathSep + pName)
                text1Lines = open(fileOrg, "r").readlines()

                # dito for text2
                text2Lines = open(fileTmp, "r").readlines()
                print
                diffLst = list(diffC.compare(text1Lines, text2Lines))
                if option == "diff":                    
                    print "Lines different in " + i[1][0] + ":"
                    for line in diffLst:
                        if line[0] == '-':
                            print line,
                elif option == "all":
                    sys.stdout.writelines(diffLst)
                print
                diffCount += 1
        else:
            print fileTmp + "\t\tNot found"
            diffCount += 1

    print
    print diffCount  
    return True

def copyAll(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def walkDir(pathVar):
    dirS = []
    fileS = []
    for path, dirs, files in os.walk(pathVar):
        for f in files:
            print path + pathSep + f + " ------ " + md5Checksum(path + pathSep + f)
            dirS.append([path, [f, md5Checksum(path + pathSep + f)]])
    return dirS

def countFiles(Barr):
    for files in os.walk(path):
        print files
    return 0

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def checkProject(pName):
    print "Checking................."

#
#delete project
#    
def delProject(pName):
    if not os.path.exists('projects' + pathSep + pName):
        print "Project not exists!: " + pName
        exit()
    shutil.rmtree('projects' + pathSep + pName)
    return True

#
#output into a file
#
def outputToFile(fileName, resultContent):
    fileTmp = open(fileName, w)
    fileTmp.close()
    return True

#
#write events to log file
#
def logEvents(logContent):

    return True

#
#update
#
def updateProject(pName):
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.config'))
    srcDir = config.get(pName,'pathS')
    version = config.get(pName,'version')

    try:
        print "Backing up..............."
        os.rename(srcDir, srcDir_ + version)
        print "Project Name:\t\t" + pName
        print "Updating................."
        createProject(pName, srcDir, version + 1)
    except:
        return False
    return True

#
#test
#
def test(pathVar):
    dirS = []
    fileS = []
    for path, dirs, files in os.walk(pathVar):
        for f in files:
            print path + pathSep + f
            dirS.append([path])
    return dirS

#
#show help
#
def help():
    for line in open("docs" + pathSep + "help.txt", "r").readlines():
        print line.replace("\n","")
    sys.exit()
