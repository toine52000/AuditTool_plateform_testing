#!/usr/bin/python3

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl

import ssl
import atexit
import sys
import requests

# disable  urllib3 warnings
if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()

class CommunicationManager:

    context = None
    si = None
    content=None
    view=None
    host, user, passwd, port = "", "", "", ""

    def __init__(self, host, user, passwd, port):

        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port

        self.getContext()
        self.connection()
        self.getContent()
        self.getView()

    def getContext(self):
        local_context = None
        
        local_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        local_context.verify_mode = ssl.CERT_NONE
        self.context = local_context

        return self.context

    def connection(self):

        if self.si is not None:
            self.deconnection()

        si = None
        try:
            si = SmartConnect(host=self.host,
                              user=self.user,
                              pwd=self.passwd,
                              port=self.port,
                              sslContext=self.context)
            self.si = si
             
        except IOError as e:
            print("Connection IOError: "+str(e))
            pass
         
        if si is None:
            print("Cannot connect to specified host using specified username and password")
            sys.exit()

        return self.si

    def getContent(self):

        try:
            self.content = self.si.RetrieveContent()

        except IOError as e:
             print("Content IOError: "+str(e))
             pass
         
        if self.si is None:
             print("Cannot deconnect the present connection")
             sys.exit()            

        return self.content
    
    def getView(self):

        try:
            objView = self.content.viewManager.CreateContainerView(self.content.rootFolder, [vim.VirtualMachine], True)
            
            vmList = objView.view
            objView.Destroy()

            self.view = vmList
        
        except IOError as e:
             print("View IOError: "+str(e))
             pass

        if self.content is None:
             print("View disable without content object")
             sys.exit()

        return self.view

    def getVmByName(self, vm_name):

        vmList = self.getView()
        vm = None
        
        for vm_obj in vmList:
            if vm_obj.name == vm_name:
                vm = vm_obj

        if (vm is None):
            print("The vm name specified doesn't exist!")
            sys.exit()
        else:
            return vm
        
    
    def deconnection(self):

        try:
            atexit.register(Disconnect, self.si)

        except IOError as e:
             print("deconnection IOError: "+str(e))
             pass
         
        if self.si is None:
             print("Cannot deconnect the present connection")
             sys.exit()

        self.si, self.content, self.view = None, None, None


    def WaitForTasks(self, tasks):
      """
      Given the service instance si and tasks, it returns after all the
      tasks are complete
      """

      pc = self.content.propertyCollector

      taskList = [str(task) for task in tasks]

      # Create filter
      objSpecs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                                                               for task in tasks]
      propSpec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                            pathSet=[], all=True)
      filterSpec = vmodl.query.PropertyCollector.FilterSpec()
      filterSpec.objectSet = objSpecs
      filterSpec.propSet = [propSpec]
      filter = pc.CreateFilter(filterSpec, True)

      try:
         version, state = None, None

         # Loop looking for updates till the state moves to a completed state.
         while len(taskList):
            update = pc.WaitForUpdates(version)
            for filterSet in update.filterSet:
               for objSet in filterSet.objectSet:
                  task = objSet.obj
                  for change in objSet.changeSet:
                     if change.name == 'info':
                        state = change.val.state
                     elif change.name == 'info.state':
                        state = change.val
                     else:
                        continue

                     if not str(task) in taskList:
                        continue

                     if state == vim.TaskInfo.State.success:
                        # Remove task from taskList
                        taskList.remove(str(task))
                     elif state == vim.TaskInfo.State.error:
                        raise task.info.error
            # Move to next version
            version = update.version
      finally:
         if filter:
            filter.Destroy()
