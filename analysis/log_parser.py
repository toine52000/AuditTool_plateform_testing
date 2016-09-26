#!/usr/local/bin/python3.5


#%System32%\winevt\Logs

from lxml import etree


class LogParser:

    lastEvent = None
    
    idEvent = None
    timeEvent = None
    
    tree = None

    newEvents = []

    def __init__(self, file_path):
        self.path = file_path
        self.tree = etree.parse(self.path)


    def determineNewEvents(self, limitID, limitDate):

                save = 0
                self.newEvents = []

                for event in self.tree.xpath("/Events/Event"):

                    if save == 1:
                        self.newEvents.append(event)
                    else:

                        tempTimeEvent=""
                        tempIDEvent=""
                        for children in event.getchildren():
                            if children.tag == "System":
                                
                                for i in children.getchildren():
                                    if i.tag == "TimeCreated":
                                        tempTimeEvent = i.get("SystemTime")
                                    if i.tag == "EventID":
                                        tempIDEvent = i.text
                                
                                if limitDate == tempTimeEvent and limitID == tempIDEvent:
                                    save = 1
        

    def determineLastEvent(self):

        self.lastEvent = None
     
        if self.tree.xpath("/Events/Event/System") is not None:
            if len(self.tree.xpath("/Events/Event/System")) > 0:
                self.lastEvent = self.tree.xpath("/Events/Event/System")[-1]

                for i in self.lastEvent.getchildren():
                    if i.tag == "TimeCreated":
                        self.timeEvent = self.tree.xpath("/Events/Event/System/TimeCreated")[-1].get("SystemTime")
                    if i.tag == "EventID":
                        self.idEvent = self.tree.xpath("/Events/Event/System/EventID")[-1].text

        return self.lastEvent

    
    def getNewEvents(self):
        return self.newEvents



    
            
        

