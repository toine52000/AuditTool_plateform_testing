#!/usr/bin/python3

from __future__ import with_statement
import atexit
import requests
import datetime
import time
import os


from pyVmomi import vim, vmodl


def upload_file(host, co_manager, vm, vm_path, vm_user, vm_pwd, args):
        creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)
        try:
                file_attribute = vim.vm.guest.FileManager.FileAttributes()
                url = co_manager.content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, creds, vm_path, file_attribute, len(args), True)
                
                url_adaptation = url.replace("*", host)
                resp = requests.put(url_adaptation, data=args, verify=False)
                
                if not resp.status_code == 200:
                        return 0
                else:
                        return 1


        except:
                return 0

def download_file(host, co_manager, vm, vm_path, vm_user, vm_pwd):

        creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)
    
                
        try:
                url = co_manager.content.guestOperationsManager.fileManager.InitiateFileTransferFromGuest(vm, creds, vm_path)
               
                url_adaptation = url.url.replace("*", host)
                resp = requests.get(url_adaptation, verify=False)
                
                if not resp.status_code == 200:
                        return 0
                else:
                        if not os.path.exists("../results/"):
                                os.system("mkdir ../results/")
                        if not os.path.exists("../results/executable/"):
                                os.system("mkdir ../results/executable/")

                        fichier = open("../results/executable/"+vm.name+"_result", "w")
                        fichier.write(resp.text)
                        fichier.close()
                        return 1
        except:
                return 0

        
        

def exec_file(co_manager, vm, vm_user, vm_pwd, path_to_program, arg):
        
        creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)
        
        try:
                pm = co_manager.content.guestOperationsManager.processManager
                ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath=path_to_program,arguments=arg)
                res = pm.StartProgramInGuest(vm, creds, ps)

                if res > 0:
                        return res
                else:
                        return 0

        except:
                return 0

def file_in_host_exist(co_manager, vm, vm_user, vm_pwd, path, file_name):

        try:
                creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)
                fm  = co_manager.content.guestOperationsManager.fileManager
                file_list = fm.ListFilesInGuest(vm, creds, path)

                ret = 0
                if len(file_list.files) > 0:
                        for a in file_list.files:
                                if a.path == file_name:
                                        ret = 1

                return ret
        except:
                return 0

def wait_end_execution(co_manager, vm, vm_user, vm_pwd, pid, wait_time_limit):

         creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)

         wait_timer=0
         while wait_timer < wait_time_limit:
                 
                pm = co_manager.content.guestOperationsManager.processManager
                exec_info = pm.ListProcessesInGuest(vm, creds)

                for process in exec_info:
                        if process.pid == pid:
                                if process.endTime != None:
                                        return 1
                                else:
                                        time.sleep(2)
                                        wait_timer +=1


         return 0


def get_file(file_path):

         with open(file_path, 'rb') as myfile:
            args = myfile.read()
         return args
