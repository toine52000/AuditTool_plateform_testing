#!/usr/bin/python3

from communication_manager import CommunicationManager
from time import gmtime, strftime

import sys

class SnapshotManager:

    def invoke_and_track(self, co_manager, func):
        try :
            task=[]
            task.append(func)
            co_manager.WaitForTasks(task)
            return 1
        except:
            return 0
        
    
    def create_snapshot(self, co_manager, vm, snapshot_name=""):

        if snapshot_name == "":
            snapshot_name = vm_name + " " +  strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        description = "Snapshot "+strftime("%Y-%m-%d %H:%M:%S", gmtime())
        dumpMemory = True
        quiesce = True
            
        ret = self.invoke_and_track(co_manager, vm.CreateSnapshot(snapshot_name, description, dumpMemory, quiesce))

        return ret
        
    def delete_snapshot(self, co_manager, vm, snapshot_name):

        snap_obj = None

        if vm.snapshot is not None:
            snapshots = self.get_snapshot_list(vm, vm.snapshot.rootSnapshotList)

        
            for snapshot in snapshots:
                if snapshot_name == snapshot.name:
                    snap_obj = snapshot.snapshot
                    print(snapshot.name+" of "+vm.name)

            if snap_obj is not None:
                ret = self.invoke_and_track(co_manager, snap_obj.RemoveSnapshot_Task(True))
            else:
                ret = 0

        else:
            ret = 0

        return ret

            
    def revert_snapshot(self, co_manager, vm, snapshot_name):

        snap_obj = None

        if vm.snapshot is not None:
            snapshots = self.get_snapshot_list(vm, vm.snapshot.rootSnapshotList)

        
            for snapshot in snapshots:
                if snapshot_name == snapshot.name:
                    snap_obj = snapshot.snapshot                

            if snap_obj is not None:
                ret = self.invoke_and_track(co_manager, snap_obj.RevertToSnapshot_Task())
            else:
                ret = 0

        else:
            ret = 0

        return ret
            
            
    def get_snapshot_list(self, vm, root, list=[]):

        snapshots = root
            
        for snapshot in snapshots:
            list.append(snapshot)

            if snapshot.childSnapshotList is not None:
                self.get_snapshot_list(vm, snapshot.childSnapshotList, list)

        return list

        

