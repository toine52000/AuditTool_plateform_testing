#!/usr/local/bin/python3.5

import sys
import os
import re

class DiffParser:
    
    parent=""
    fils=""

    inputFile = ""
    outputFile = ""

    createdFiles = []
    deletedFiles = []
    modifiedFiles = []
    modifiedBinaries = []
    modifiedText = []

    modifiedRegistry = []
    modifiedLogFile = []

    def __init__(self, diffFile, parentSnap, sonSnap):
        self.inputFile = diffFile
        self.parent = parentSnap
        self.fils = sonSnap
    
    def parseDiffResultFile(self):

        self.createdFiles = []
        self.deletedFiles = []
        self.modifiedBinaries = []
        self.modifiedText = []
        self.modifiedFiles = []
        self.modifiedRegistry = []
        self.modifiedLogFile = []

        with open(self.inputFile, 'r') as myfile:

            for line in myfile:

                #*deleting   Windows/... -> fichier cree  
                #>f+++++++++ Windows/... -> fichier supprime
                #>f..t...... Windows/... -> fichier modifie

                """crea_re = re.compile('^\*deleting   (.*[^\/]+)\n$')
                del_re = re.compile('^>f\+\+\+\+\+\+\+\+\+ (.*[^\/])\n$')
                modi_re = re.compile('^>f\.\.t\.\.\.\.\.\. (.*[^\/])\n$')

                 # Creation of a file detected
                if crea_re.match(line) is not None:
                    fichier = crea_re.match(line).group(1)
                    self.createdFiles.append("/"+fichier)
                    
                # Removal of a file detected
                elif del_re.match(line) is not None:
                    fichier = del_re.match(line).group(1)
                    self.deletedFiles.append("/"+fichier)

                # Different binary files detected
                elif modi_re.match(line) is not None:
                    fichier = modi_re.match(line).group(1)
                    print(fichier)                 
                    self.modifiedFiles.append("/"+fichier)

                    if self.isARegistry(fichier):
                            self.modifiedRegistry.append("/"+fichier)

                    if self.isALogFile(fichier):
                            self.modifiedLogFile.append("/"+fichier)"""

                    

                p = re.compile('^Seulement dans '+self.fils+'(.*): (.*)$')
                a = re.compile('^Seulement dans '+self.parent+'(.*): (.*)$')
                b = re.compile('^Les fichiers binaires '+self.fils+'(.*) et '+self.parent+'(.*) sont differents$')
                c = re.compile('^Les fichiers binaires '+self.parent+'(.*) et '+self.fils+'(.*) sont differents$')
                d = re.compile('diff -r '+self.parent+'(.*) '+self.fils+'(.*)')
                e = re.compile('diff -r '+self.fils+'(.*) '+self.parent+'(.*)')
                f = re.compile('^Les fichiers '+self.fils+'(.*) et '+self.parent+'(.*) sont differents$')
                g = re.compile('^Les fichiers '+self.parent+'(.*) et '+self.fils+'(.*) sont differents$')

                # Creation of a file detected
                if p.match(line) is not None:
                    dossier =  p.match(line).group(1)
                    fichier =  p.match(line).group(2)
                    self.createdFiles.append(dossier+"/"+fichier)

                # Removal of a file detected
                elif a.match(line) is not None:
                    dossier =  a.match(line).group(1)
                    fichier =  a.match(line).group(2)
                    self.deletedFiles.append(dossier+"/"+fichier)

                # Different binary files detected
                elif b.match(line) is not None:
                    fichier1 =  b.match(line).group(1)
                    fichier2 =  b.match(line).group(2)

                    if fichier1 == fichier2:
                        self.modifiedBinaries.append("/"+fichier1)

                elif c.match(line) is not None:
                    fichier1 =  c.match(line).group(1)
                    fichier2 =  c.match(line).group(2)

                    if fichier1 == fichier2:
                        self.modifiedBinaries.append("/"+fichier1)

                # Different text files detected
                elif d.match(line) is not None:
                    fichier1 =  d.match(line).group(1)
                    fichier2 =  d.match(line).group(2)

                    if fichier1 == fichier2:
                        self.modifiedText.append("/"+fichier1)

                elif e.match(line) is not None:
                    fichier1 =  e.match(line).group(1)
                    fichier2 =  e.match(line).group(2)

                    if fichier1 == fichier2:
                        self.modifiedText.append("/"+fichier1)


                # Different files detected
                elif f.match(line) is not None:
                    fichier1 = f.match(line).group(1)
                    fichier2 = f.match(line).group(2)

                    if fichier1 == fichier2:
                        self.modifiedFiles.append("/"+fichier1)
                        
                        if self.isARegistry(fichier1):
                            self.modifiedRegistry.append("/"+fichier1)

                        if self.isALogFile(fichier1):
                            self.modifiedLogFile.append("/"+fichier1)

                elif g.match(line) is not None:
                    fichier1 = g.match(line).group(1)
                    fichier2 = g.match(line).group(2)

                    if fichier1 == fichier2:
                        self.modifiedFiles.append(fichier1)

                        if self.isARegistry(fichier1):
                            self.modifiedRegistry.append(fichier1)
                            
                        if self.isALogFile(fichier1):
                            self.modifiedLogFile.append(fichier1)
                        

    def isARegistry(self, path_file):
        return {
            #Windows 7-8-10
            "Windows/System32/config/SYSTEM" : True,
            "Windows/System32/config/SAM" : True,
            "Windows/System32/config/SECURITY" : True,
            "Windows/System32/config/SOFTWARE" : True,
            "Windows/System32/config/DEFAULT" : True
            }.get(path_file, False)

    def isALogFile(self, path_file):
        a = re.compile('^Windows/System32/winevt/Logs/.*\.evtx$')
        if a.match(path_file) is not None:
            return True
        else:
            return False

    def getModifiedLogFile(self):
        return self.modifiedLogFile
        
    def getModifiedRegistries(self):
        return self.modifiedRegistry
	
    def getCreatedFiles(self):
        return self.createdFiles

    def getModifiedFiles(self):
        return self.modifiedFiles

    def getDeletedFiles(self):
        return self.deletedFiles

    def getModifiedRegistry(self):
        return  self.modifiedRegistry

    def printDiffResult(self):

        if len(self.createdFiles) > 0:
            print("Fichiers crees:")
            for i in self.createdFiles:
                print(i)
            print("")

        if len(self.deletedFiles) > 0:
            print("Fichiers supprimes:")
            for i in self.deletedFiles:
                print(i)
            print("")

        if len(self.modifiedBinaries) > 0:
            print("Fichiers binaires modifies:")
            for i in self.modifiedBinaries:
                print(i)
            print("")

        if len(self.modifiedText) > 0:
            print("Fichier textes modifies:")
            for i in self.modifiedText:
                print(i)
            print("")

        if len(self.modifiedFiles) > 0:
            print("Fichier modifies:")
            for i in self.modifiedFiles:
                print(i)
            print("")
