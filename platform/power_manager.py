#!/usr/bin/python3

from pyVmomi import vim, vmodl
from communication_manager import CommunicationManager

#TODO gérer les erreurs de guest tools non disponible

class PowerManager:
  
   def power_on(self, co_manager, vm):

         try:
            tasks = [vm.PowerOn()]
            co_manager.WaitForTasks(tasks)
            return 1

         except vim.fault.InvalidPowerState:
            return self.reboot(co_manager, vm)
         except vim.fault.RuntimeFault as e:
            print("Communication impossible, please reconnect and retry: "+str(e))
            sys.exit()
         except:
            print("Unexpected Error during Powered On")
            return 0

   def power_off(self, co_manager, vm):

         try:
            tasks = [vm.PowerOff()]
            co_manager.WaitForTasks(tasks)
            return 1

         except vim.fault.InvalidPowerState:
            return 1
            pass
         except vim.fault.RuntimeFault as e:
            print("Communication impossible, please reconnect and retry: "+str(e))
            sys.exit()
         except:
            print("Unexpected Error during Powered On")
            return 0
            
   def reboot(self, co_manager, vm):
      
         try:
            tasks = [vm.ResetVM_Task()]
            co_manager.WaitForTasks(tasks)
            return 1

         except vim.fault.InvalidPowerState:
            return self.power_on(co_manager, vm)
         except vim.fault.RuntimeFault as e:
            print("Communication impossible, please reconnect and retry: "+str(e))
            sys.exit()
         except vim.fault.ToolsUnavailable as e:
            print("VMWare Guest Tool are not Running, please reinstall all the VMs")
            return 0
         except:
            print("Unexpected Error during Powered On")
            return 0
            


   def shutdown(self, co_manager, vm_name):

         #TODO################################
         vmList = co_manager.view
         
         # Find the vm and power it on
         tasks = [vm.ShutdownGuest() for vm in vmList if vm.name in vm_name]

         # Wait for power on to complete
         co_manager.WaitForTasks(tasks)

         print("Virtual Machine(s) have been shutdown successfully: "+vm.name)
