#!/usr/local/bin/python3.5

import sys
import os
import re
import codecs
import subprocess


### Import python-registry (galère!) et lxml
# Modifier la lib python-registry
#dans RegistryParser.py
# s = s.decode("utf16") =>             try:
#                                          s = s.decode("utf16")
#                                      except AttributeError:
#                                          s = s
#

from Registry import *
from diff_results_parser import DiffParser
from xml_creator import XmlCreator
from registry_parser import RegistryParser, RegistryComparator
from log_parser import LogParser
from xml_comparator import XmlComparator

class SnapshotAnalysis:
    snap_grandFather=""
    snap_father=""
    snap_son=""

argument = sys.argv[1]
    
def main():

    user = "root"
    passwd = "CYKUG6dtQ0uX"
    ipHost="10.200.16.239"
    datastore = "~/vmfs/volumes/datastore1/"
    xml_result_files = []

    vmnames = []
    vmnames = get_vm_list(argument)
    #vmnames.append("w7_home_premium_x86")

    # Installation des différents répertoire de travail (../results/*)
    print("Prepare work path")
    #prepareWorkPath()

    for vmname in vmnames:

        print("#################################################################")
        print("########################## Analyse ##############################")
        print("#################################################################")

        ##################################################################
        # Préparation ###################################################
        ##################################################################
        print("Delete useless files")
        unmountSnapshot()
        removeUselessFiles()
        
        # Récupération des snapshot sur le serveur ESXi 
        print("Get data file i.e. snapshots")
        getDiffDataFile(user, passwd, ipHost, datastore, vmname)
        
        # On détermine l'ordre de parenté des snapshots pour connaître leur sens de lecture
        print("Determine the order of the different snapshot")
        determineSnapOrder()
        
        # On monte les systèmes de fichier contenu dans les snapshots
        print("Mount file system")
        mountSnapshot(SnapshotAnalysis.snap_grandFather, SnapshotAnalysis.snap_father, SnapshotAnalysis.snap_son)
        
        # On instentie les objets utilisés plus tard
        xml_execution = XmlCreator(vmname, "execution")
        xml_reboot = XmlCreator(vmname, "reboot")
        
        parser_execution = DiffParser("../results/diff/diffExecution_"+vmname, "../results/mnt/initial/", "../results/mnt/execution/")    
        parser_reboot = DiffParser("../results/diff/diffReboot_"+vmname, "../results/mnt/execution/", "../results/mnt/reboot/")
        
        
        ##################################################################
        # Différence sur les systèmes de fichiers ########################
        ##################################################################
        
        # Analyse des différences du système de fichier via la commande diff et création des fichiers résultats (results/diff/)
        print("Create diff files")
        diffFileSytem("../results/mnt/initial/", "../results/mnt/execution/", "../results/diff/diffExecution_"+vmname)
        diffFileSytem("../results/mnt/execution/", "../results/mnt/reboot/", "../results/diff/diffReboot_"+vmname)

        if os.path.exists("../results/diff/diffExecution_"+vmname):
            print("Parsing of execution diff results")
            parser_execution.parseDiffResultFile()        
            xml_execution.create_files_system_node(parser_execution)
            
            if os.path.exists("../results/diff/diffReboot_"+vmname):
                print("Parsing of reboot diff results")
                parser_reboot.parseDiffResultFile()        
                xml_reboot.create_files_system_node(parser_reboot)
                
                
        ##################################################################
        # Différence sur les registres ###################################
        ##################################################################
        print("Registry files comparaison")
        modifiedRegistry_execution = parser_execution.getModifiedRegistries()
        modifiedRegistry_reboot = parser_reboot.getModifiedRegistries()
    
        for path in modifiedRegistry_execution:
            reg1 = Registry.Registry("../results/mnt/initial/"+path)
            reg2 = Registry.Registry("../results/mnt/execution/"+path)

            rp1 = RegistryParser()
            rp1.registry_data_extractor(reg1.root(), 0)

            rp2 = RegistryParser()
            rp2.registry_data_extractor(reg2.root(), 0)

            rc = RegistryComparator(rp1.getRegistryDictPath(), rp2.getRegistryDictPath())
            rc.registry_comparator()
            xml_execution.create_registry_modification_node(path, rc)

        for path in modifiedRegistry_reboot:
            reg3 = Registry.Registry("../results/mnt/execution/"+path)
            reg4 = Registry.Registry("../results/mnt/reboot/"+path)

            rp3 = RegistryParser()    
            rp3.registry_data_extractor(reg3.root(), 0)

            rp4 = RegistryParser()    
            rp4.registry_data_extractor(reg4.root(), 0)

            rc2 = RegistryComparator(rp3.getRegistryDictPath(), rp4.getRegistryDictPath())
            rc2.registry_comparator()
            xml_reboot.create_registry_modification_node(path, rc2)

        ##################################################################
        # Différence sur les logs ########################################
        ##################################################################
        print("Logs files comparaison")
        modifiedLog_execution = parser_execution.getModifiedLogFile()
        modifiedLog_reboot = parser_reboot.getModifiedLogFile()

        #Pour tous les fichiers de logs modifiés durant execution
        for logFile in modifiedLog_execution:

            # I - Récupération de l'ID et date du dernier event logué
            fileName = logFile.split("/")
            filePath = "../results/logs/initial_"+vmname+"_"+fileName[-1].replace(" ","_")

            #On créé les fichiers XML des données de chaque fichier de logs
            os.system("./get_log_xml.py \"../results/mnt/initial/"+logFile+"\" | sed \'s/ xmlns=\"[^\"]*\"//\' > \""+filePath+"\"")
            
            logParser_initial = LogParser(filePath)
            logParser_initial.determineLastEvent()

            # II - Récupération de l'ensemble des events suivants le dernier event repéré précédent
            filePath = "../results/logs/execution_"+vmname+"_"+fileName[-1].replace(" ","_")
        
            os.system("./get_log_xml.py \"../results/mnt/execution/"+logFile+"\" | sed \'s/ xmlns=\"[^\"]*\"//\' > \""+filePath+"\"")

            logParser_execution = LogParser(filePath)
            logParser_execution.determineNewEvents(logParser_initial.idEvent, logParser_initial.timeEvent)
            addedNodes = logParser_execution.getNewEvents()

            xml_execution.create_log_modification_node(logFile, addedNodes)

        #Pour tous les fichiers de logs modifiés durant reboot
        for logFile in modifiedLog_reboot:

            # I - Récupération de l'ID et date du dernier event logué
            fileName = logFile.split("/")
            filePath = "../results/logs/execution_"+vmname+"_"+fileName[-1].replace(" ","_")

            #On créé les fichiers XML des données de chaque fichier de logs
            os.system("./get_log_xml.py \"../results/mnt/execution/"+logFile+"\" | sed \'s/ xmlns=\"[^\"]*\"//\' > \""+filePath+"\"")
            
            logParser_execution = LogParser(filePath)
            logParser_execution.determineLastEvent()

            # II - Récupération de l'ensemble des events suivants le dernier event repéré précédent
            filePath = "../results/logs/reboot_"+vmname+"_"+fileName[-1].replace(" ","_")
        
            os.system("./get_log_xml.py \"../results/mnt/reboot/"+logFile+"\" | sed \'s/ xmlns=\"[^\"]*\"//\' > \""+filePath+"\"")

            logParser_reboot = LogParser(filePath)
            logParser_reboot.determineNewEvents(logParser_execution.idEvent, logParser_execution.timeEvent)
            addedNodes = logParser_reboot.getNewEvents()

            xml_reboot.create_log_modification_node(logFile, addedNodes)
         
    
        ##################################################################
        # Création du XML résultat #######################################
        ##################################################################
        print("Create results XML files")    
        xml_execution.create_xml_file()
        xml_result_files.append(vmname+"_execution.xml")
        xml_reboot.create_xml_file()
        xml_result_files.append(vmname+"_reboot.xml")

        ##################################################################
        # Action post-analyse (on range les jouets!) #####################
        ##################################################################
    
        print("Unmount file system")
        unmountSnapshot()
    
        print("Delete useless files")
        removeUselessFiles()

    
    ##################################################################
    # Différence avec les références #################################
    ##################################################################
    print("Difference with the normal behaviour")
    for xml_result in xml_result_files:

        #Si pas de fichier de référence, il devient une nouvelle référence
        if not os.path.exists("../results/references_xml/"+xml_result):
            if os.path.exists("../results/xml_result/"+xml_result):
                os.system("cp ../results/xml_result/"+xml_result+" ../results/references_xml/"+xml_result)

        #Si le fichier de référence est présent, comparaison
        else:
            if os.path.exists("../results/xml_result/"+xml_result):
                xml_comparator = XmlComparator("../results/references_xml/"+xml_result, "../results/xml_result/"+xml_result)
                xml_comparator.compare_xml()
                xml_comparator.create_result_file()
    print("Finish!")




    
#Récupère les snapshots pris lors de la phase de tests précedentes directement sur le serveur ESXi
def getDiffDataFile(user, passwd, ipHost, datastore, vmname):
    os.system("sshpass -p \""+passwd+"\" scp "+user+"@"+ipHost+":"+datastore+vmname+"/*.vmdk ../results/snapshots/1/")
    os.system("cp -R ../results/snapshots/1/* ../results/snapshots/2/")
    os.system("cp -R ../results/snapshots/1/* ../results/snapshots/3/")

#S'assure de la présence de l'ensemble des sous-répertoires utiles à l'analyse (absent lors de la première exécution)
def prepareWorkPath():

    # Prepare results 
    if not os.path.exists("../results/"):
        os.system("mkdir ../results/")
    
    # Prepare copy of snapshot
    if not os.path.exists("../results/snapshots/"):
        os.system("mkdir ../results/snapshots/")
    if not os.path.exists("../results/snapshots/1/"):
        os.system("mkdir ../results/snapshots/1/")
    if not os.path.exists("../results/snapshots/2/"):
        os.system("mkdir ../results/snapshots/2/")
    if not os.path.exists("../results/snapshots/3/"):
        os.system("mkdir ../results/snapshots/3/")
 
    #Prepare mount point
    if not os.path.exists("../results/mnt/"):
        os.system("mkdir ../results/mnt/")
    if not os.path.exists("../results/mnt/initial/"):
        os.system("mkdir ../results/mnt/initial")
    if not os.path.exists("../results/mnt/execution/"):
        os.system("mkdir ../results/mnt/execution/")
    if not os.path.exists("../results/mnt/reboot/"):
        os.system("mkdir ../results/mnt/reboot/")
    if not os.path.exists("../results/mnt/reboot/"):
        os.system("mkdir ../results/mnt/reboot/")

    #Prepare diff results
    if not os.path.exists("../results/diff/"):
        os.system("mkdir ../results/diff/")

    #Prepare logs file parsing results
    if not os.path.exists("../results/logs/"):
        os.system("mkdir ../results/logs/")
        
    #Prepare XML output file
    if not os.path.exists("../results/xml_result/"):
        os.system("mkdir ../results/xml_result/")

    #Prepare XML differences between results and normal behaviour
    if not os.path.exists("../results/references_diff_result/"):
        os.system("mkdir ../results/references_diff_result/")

    if not os.path.exists("../results/readable_result/"):
        os.system("mkdir ../results/readable_result/")

    os.system("sudo chmod -R 777 ../results/")


#Monte les 3 snapshots récupérés directement sur le disque dur
def mountSnapshot(grandFatherSnap, fatherSnap, sonSnap):
    os.system("sudo vmware-mount ../results/snapshots/1/"+grandFatherSnap+" 1 ../results/mnt/initial/")
    os.system("sudo vmware-mount ../results/snapshots/2/"+fatherSnap+" 1 ../results/mnt/execution/")
    os.system("sudo vmware-mount ../results/snapshots/3/"+sonSnap+" 1 ../results/mnt/reboot/")

#Lance la commande diff sur 2 snapshots montés récédement
def diffFileSytem(parentSnapMountPoint, sonSnapMountPoint, outputFile):
    os.system("sudo diff -r -q "+parentSnapMountPoint+" "+sonSnapMountPoint+" > "+outputFile)
    #os.system("sudo rsync -anv "+parentSnapMountPoint+" "+sonSnapMountPoint+" --itemize-changes --delete > "+outputFile+" 2> /dev/null")

#Démonte l'ensemble des snapshots montés précédement
def unmountSnapshot():
    os.system("sudo vmware-mount -x")

#Supprime les fichiers lors de l'analyse et inutile a posteriori
def removeUselessFiles():
    os.system("rm -rf ../results/snapshots/1/*")
    os.system("rm -rf ../results/snapshots/2/*")
    os.system("rm -rf ../results/snapshots/3/*")
    os.system("rm -rf ../results/diff/*")
    return 0

#Determine l'odre de création des snapshots (qui ne correspond pas forcément à leur nom)
#afin de les monter dans le bon sens
def determineSnapOrder():

    listFileDir = os.listdir("../results/snapshots/1/")
    listFile = []
    regex = re.compile("disk-[0-9]*\.vmdk$")
    for i in listFileDir:
        if regex.match(i):
            listFile.append(i)
    
    
    #Find the grandfather - Snapshot intial / taking before execution
    SnapshotAnalysis.snap_grandFather = ""

    for inputFile in listFile:
        file = codecs.open("../results/snapshots/1/"+inputFile, 'r', encoding='utf-8')
        data = file.read()
        if "parentFileNameHint=\"disk.vmdk\"" in data:
            SnapshotAnalysis.snap_grandFather = inputFile
        file.close()        

    #Find the father - Snapshot execution / taking after execution
    SnapshotAnalysis.snap_father = ""

    for inputFile in listFile:
        file = codecs.open("../results/snapshots/1/"+inputFile, 'r', encoding='utf-8')
        data = file.read()
        if "parentFileNameHint=\""+SnapshotAnalysis.snap_grandFather+"\"" in data:
            SnapshotAnalysis.snap_father = inputFile
        file.close() 

    #Find the son - Snapshot reboot / taking before reboot
    SnapshotAnalysis.snap_son = ""

    for inputFile in listFile:
        file = codecs.open("../results/snapshots/1/"+inputFile, 'r', encoding='utf-8')
        data = file.read()
        if "parentFileNameHint=\""+SnapshotAnalysis.snap_father+"\"" in data:
            SnapshotAnalysis.snap_son = inputFile
        file.close() 

    print("Le gd-pere: "+SnapshotAnalysis.snap_grandFather)
    print("Le père: "+SnapshotAnalysis.snap_father)
    print("le fils: "+SnapshotAnalysis.snap_son)
    
    
    return 0

def get_vm_list(argument):

    vm_list = []
    
    name_list = argument.split(';')
    for name in name_list:
        print(name)
        vm_list.append(name)

    return vm_list

# Start program
if __name__ == "__main__":
    main()
