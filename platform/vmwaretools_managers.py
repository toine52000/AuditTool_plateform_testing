#!/usr/bin/python3

from pyVim import connect
from pyVmomi import vim, vmodl

import time

def guest_tools_runnings_status(vm):
    
    wait_timer = 0
    
    while vm.guest.toolsRunningStatus != "guestToolsRunning":
        wait_timer += 1
        time.sleep(2)
        if wait_timer > 40:
            #print("Guest tools are not running")
            return 0
    
    #print("Guest tools are running")
    return 1

def guest_tools_status(co_manager, vm):
    
    tools_status = vm.guest.toolsVersionStatus2
    
    if (tools_status == 'guestToolsSupportedOld'or
         tools_status == 'guestToolsNeedUpgrade'):
         #print("Guest Tools must be upgrade!")

         #task = vm.UpgradeTools_Task()
         #Server.co.wait_for_task(module, task)

         return 1
    
    elif(tools_status == 'guestToolsCurrent' or
         tools_status == 'guestToolsSupportedNew' or
         tools_status == 'guestToolsUnmanaged'):            
         #print("Guest Tools is up to date")
         return 1
    
    elif tools_status == 'guestToolsTooNew':
         #print('tools too new for this host')
         return 0

    elif tools_status == 'guestToolsBlacklisted':
         #print('tools are blacklisted for this host')
         return 0

    elif tools_status == 'guestToolsNotInstalled':
         #print('tools are not installed')
         return 0

    elif tools_status == 'guestToolsTooOld':
         #print('tools too old. install manually')
         return 0

    else:
        return 0
         #print('tools upgrade failed')

def test_tools_availability(co_manager, vm):

    rs = guest_tools_runnings_status(vm)
    ts =  guest_tools_status(co_manager, vm)

    if (rs == 1 and ts == 1):
        return 1
    else:
        return 0

    
