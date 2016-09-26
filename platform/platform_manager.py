#!/usr/bin/python3

from power_manager import PowerManager
from communication_manager import CommunicationManager
from snapshot_manager import SnapshotManager
from file_manager import upload_file, download_file, exec_file, file_in_host_exist, wait_end_execution, get_file
from vmwaretools_managers import guest_tools_runnings_status, guest_tools_status, test_tools_availability
from pyVmomi import vim, vmodl

import sys
import os
import time
from math import ceil

#Prise de la liste des VM à utiliser par argument de la forme "vm1;vm2;vm3"
vm_argument = sys.argv[1]

class Server:
    HOST="10.200.16.239"
    USER="root"
    PASSWD="CYKUG6dtQ0uX"
    PORT=443

    VM_USER="vagrant"
    VM_PASS="vagrant"

    co = None

    FROM_FILE="upload_files/audit_tool.exe"
    FROM_FILE_X64="upload_files/audit_tool_x64.exe"

    TO_DIRECTORY="C:\\"
    TO_FILE="audit_tool.exe"
    TO_PATH=TO_DIRECTORY+TO_FILE

    RESULT_DIRECTORY="C:\\"
    RESULT_FILE="resultat"
    RESULT_PATH=RESULT_DIRECTORY+RESULT_FILE

    CMD="C:\\audit_tool.exe"
    PARAM="-o "+RESULT_PATH

class Error:
    vm=[]
    step=[]

class Run:
    vmList = []
    step = 1
    cpt = 0 
    nbVM = 0
    tempVmList = []
    presentVmList = []

def main():

 vm_to_analysis = []
    
 #Initialisation
 Server.co = CommunicationManager(Server.HOST, Server.USER, Server.PASSWD, Server.PORT)
 power_manager=PowerManager()
 snapshot_manager = SnapshotManager()
 

  #Compter les VMs
 #Run.vmList = Server.co.getView()
 Run.vmList = get_vm_list(vm_argument, Server.co)
 Run.nbVM = len(Run.vmList)



 print("###########################################################################")
 print("############## BIENVENUE DANS L'AUDITTOOL-TESTING-PLATFORM ################")
 print("###########################################################################")
 print("La plate-forme utilisera  "
       +str(Run.nbVM) +" machines virtuelles")
 print("Les tests seront applique en vagues de "+str(Run.step)+" VMs")

 wave=1
 #Boucle principale
 while Run.cpt != Run.nbVM:

     print("\nVague numero "+str(wave)+":")
     wave+=1
     

     
     #Creation d'une liste restreintes de VMs pour optimisation
     Run.tempVmList = []
     if (Run.cpt+Run.step) <= Run.nbVM:
         for i  in range(Run.cpt, Run.cpt+Run.step):
             if Run.vmList[i].name != "server":
                 Run.tempVmList.append(Run.vmList[i])
         Run.cpt+=Run.step
             
     else:
         for i in range(Run.cpt, Run.nbVM):
             if Run.vmList[i].name != "server":
             	 Run.tempVmList.append(Run.vmList[i])
         Run.cpt=Run.nbVM

     print("Cette vague s'appliquera au editions Windows suivantes:")
     for vm in Run.tempVmList:
         print(vm.name+" / ", end='')
     print("")
     print("")


     os.system("date")    
     #Retour des VM à l'etat initial
     print("0 - Return to initial state...")
     for vm in Run.tempVmList:
         ret = power_manager.power_off(Server.co, vm)

         try:
             snapshot_manager.delete_snapshot(Server.co, vm, "snapshot_execution")
             snapshot_manager.delete_snapshot(Server.co, vm, "snapshot_reboot")
             snapshot_manager.delete_snapshot(Server.co, vm, "snapshot_useless")
         except:
             pass
         
         ret2 = snapshot_manager.revert_snapshot(Server.co, vm, "snapshot_initial")

         if ret == 0 or ret2 == 0:
             add_error(0, vm)
     check_error(0)
             


     #Allumer les VMs
     #print("1 - Power on the VMs...")
     #for vm in Run.tempVmList:
     #    ret =  power_manager.power_on(Server.co, vm)
     #    if ret == 0:
     #        add_error(1, vm)
     #check_error(1)


             
     #Attente de l'initialisation des VMs.
     #print("2 - Waiting for complete starting...")
     #time.sleep(45)
     #check_error(2)

     
     os.system("date")    
     #Verification de bon fonctionnement des guest tools
     print("1 - Check the VMWare guest tools availability...")
     for vm in Run.tempVmList:
         if (test_tools_availability(Server.co, vm) != 1):
                 add_error(1, vm)
     check_error(1)

     
     os.system("date")    
     #Envoie le fichier
     print("2 - Sends the executable file...")
     file_to_upload = get_file(Server.FROM_FILE)
     file_to_upload_x64 = get_file(Server.FROM_FILE_X64)
     
     for vm in Run.tempVmList:

         if "x86" in vm.name:
             ret = upload_file(Server.HOST, Server.co, vm, Server.TO_PATH,
                               Server.VM_USER, Server.VM_PASS, file_to_upload)
         elif "x64" in vm.name:
             ret = upload_file(Server.HOST, Server.co, vm, Server.TO_PATH,
                               Server.VM_USER, Server.VM_PASS, file_to_upload_x64)
         else:
             print("The name of the VM doesn't respect the normal name"
                   "(\"version_edition_architecture[_SP]\""
                   "-> exemple: w7_professional_x86_SP1)")
             print("Please reinstall the VMs")

         ret2 = file_in_host_exist(Server.co, vm, Server.VM_USER, Server.VM_PASS,
                                   Server.TO_DIRECTORY, Server.TO_FILE)
         
         if(ret != 1 or ret2 != 1):
             add_error(2, vm)
     check_error(2)

     os.system("date")    
     #Snapshot intermediaire
     print("3 - Take intermediate snapshot  (execution snapshot)...")
     for vm in Run.tempVmList:
         ret = snapshot_manager.create_snapshot(Server.co, vm, "snapshot_execution")

         if(ret != 1):
             add_error(3, vm)
     check_error(3)

     os.system("date")    
     #lancement de l'execution du fichier
     print("4 - Execute the file...")
     pid=[]
     for vm in Run.tempVmList:
         
         ret = exec_file(Server.co, vm, Server.VM_USER, Server.VM_PASS,
                         Server.CMD, Server.PARAM)

         if(ret==0):
             add_error(4, vm)
         else:
             pid.append(ret)
     check_error(4)


     os.system("date")    
     #Attente de fin d'execution
     print("5 - Wait end of the execution...")
     id=0
     for vm in Run.tempVmList:
         ret = wait_end_execution(Server.co, vm, Server.VM_USER, Server.VM_PASS,
                                  pid[id], 600)
         ret2 = file_in_host_exist(Server.co, vm, Server.VM_USER, Server.VM_PASS,
                                   Server.RESULT_DIRECTORY, Server.RESULT_FILE)
         
         if ret == 0 or ret2 == 0:
              add_error(5, vm)

         id+=1
     check_error(5)

     os.system("date")    
     #Snapshot intermediaire
     print("6 - Take intermediate snapshot (reboot snapshot)...")
     for vm in Run.tempVmList:
         ret = snapshot_manager.create_snapshot(Server.co, vm, "snapshot_reboot")

         if(ret != 1):
             add_error(6, vm)
     check_error(6)
    
     os.system("date")    
     #Extraction des resultats
     print("7 - Extraction of execution results...")
     for vm in Run.tempVmList:
         ret = download_file(Server.HOST, Server.co, vm, Server.RESULT_PATH,
                             Server.VM_USER, Server.VM_PASS)

         if(ret != 1):
             add_error(7, vm)
     check_error(7)

     os.system("date")    
     #Reboot
     print("8 - Reboot...")
     for vm in Run.tempVmList:
         ret = power_manager.reboot(Server.co, vm)

         if ret != 1:
             add_error(8, vm)
     check_error(8)

     os.system("date")    
     #Attente reboot complet
     print("9 - Waiting for complete reboot...")
     time.sleep(60)
     check_error(9)

     os.system("date")    
     #Snapshot intermediaire
     print("10 - Take final snapshot... (rubbish snapshot)")
     for vm in Run.tempVmList:
         ret = snapshot_manager.create_snapshot(Server.co, vm, "snapshot_useless")

         if(ret != 1):
             add_error(10, vm)
     check_error(10)

     os.system("date")    
     #Eteindre les VMs
     print("11 - Poweroff...")
     for i  in range(Run.cpt-Run.step, Run.cpt):
         vm = Run.vmList[i]
         
         if vm.name != "server":
             ret = power_manager.power_off(Server.co, vm)

         if ret != 1:
             add_error(11, vm)
     check_error(11)
     vm_to_analysis += Run.tempVmList 

         
 #Donnexion            
 Server.co.deconnection()
 resume_error()

 arg = ""
 for vm in vm_to_analysis:
     arg += vm.name+";"
 os.system("../analysis/snap_analysis.py "+arg)
 
 


def add_error(error_step, vm):

    Error.vm.append(vm)
    Error.step.append(error_step)
    Run.tempVmList.remove(vm)

def resume_error():

    step_name = ["Return to initial state",
                 "Check the VMWare guest tools availability",
                 "Sends the executable file",
                 "Take intermediate snapshot (execution snapshot)",
                 "Execute the file",
                 "Wait end of the execution",
                 "Take intermediate snapshot (reboot snapshot)",
                 "Extraction of execution result",           
                 "Reboot",
                 "Waiting for complete reboot",
                 "Take final snapshot (rubbish snapshot)",
                 "Poweroff"]
    
    if len(Error.step) ==  0:
        print("")
        print("Successfully completed with no error!")
        print("")

    else:
        print("")
        for i in range(0, len(Error.step)):
            print("An error occured in the step \"" + str(Error.step[i])
                  +": "+step_name[Error.step[i]]
                  +"\" with the virtual machine named "
                  + Error.vm[i].name)
        print("")
        print("Please verify this(ese) VM(s) directly in the ESXi server")
        print("Although, the script have still used the others VMs correctly")
    
    
def check_error(error_step):

    step_name = ["Return to initial state",
                 "Check the VMWare guest tools availability",
                 "Sends the executable file",
                 "Take intermediate snapshot (execution snapshot)",
                 "Execute the file",
                 "Wait end of the execution",
                 "Take intermediate snapshot (reboot snapshot)",
                 "Extraction of execution result",           
                 "Reboot",
                 "Waiting for complete reboot",
                 "Take final snapshot (rubbish snapshot)",
                 "Poweroff"]
    
    #Si une erreur est deja apparu
    if len(Error.step) > 0:
        error_cpt = 0
        
        for a in Error.step:
            if a == error_step:
                error_cpt +=1

        #Toute la vague à loupe    
        if error_cpt == Run.step:
            print("[-] "+step_name[error_step])
            print("An unexpected error has occurred, no action are possible,"
                  " please reinstall all the VM and check your network before"
                  " to run this script")
            sys.exit()

        #Toute la vague à reussi
        elif error_cpt == 0:
            print("[+] "+step_name[error_step])

        else:
            print("[~] "+step_name[error_step])

    #Si pas encore d'erreur
    else:
        print("[+] "+step_name[error_step])
            

def get_vm_list(argument, co_manager):

    vm_list = []
    
    name_list = argument.split(';')
    for name in name_list:
        print(name)
        vm_list.append(co_manager.getVmByName(name))

    return vm_list


# Start program
if __name__ == "__main__":
    main()
