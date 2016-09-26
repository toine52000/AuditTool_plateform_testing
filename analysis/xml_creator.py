#!/usr/local/bin/python3.5

from lxml import etree
from registry_parser import RegistryComparator
from diff_results_parser import DiffParser

class XmlCreator:

    
    def __init__(self, vm_name, step_name):

        #Node XML
        self.analysis_node  = etree.Element("analysis")
        self.files_system_node = None
        self.added_file_node = None
        self.deleted_file_node = None
        self.modified_file_node = None
        self.registry_modification_node = None

        self.log_added_event = None

        #Nom du fichier XML de sortie
        self.vm_name = vm_name
        self.step_name = step_name

        
    def create_xml_file(self):
        
        try:
            output_xml = open("../results/xml_result/"+self.vm_name+"_"+self.step_name+".xml", "w")
            output_xml.write(str(etree.tounicode(self.analysis_node, pretty_print=True)))
            output_xml.close()
        except IOError as e:
            print(e)

            
    def create_files_system_node(self, diff_parser_obj):

        created_files = diff_parser_obj.createdFiles
        deleted_files = diff_parser_obj.deletedFiles
        modified_files = diff_parser_obj.modifiedFiles
        
        #Création de la node files_system
        if len(created_files) != 0 or len(deleted_files) != 0 or len(modified_files) != 0:
            self.files_system_node = etree.SubElement(self.analysis_node, "files_system")

            #Création de la sous-node "added_files"
            if len(created_files) != 0:
                self.added_file_node = etree.SubElement(self.files_system_node, "added_file")

                #Création des sous-nodes fichiers créés
                for i in created_files:

                    name_formated = self.group_file_path(i)[0]
                    path_formated = self.group_file_path(i)[1]
                    
                    file_node = etree.SubElement(self.added_file_node, "file")
                    name = etree.SubElement(file_node, "name")
                    name.text = name_formated

                    path = etree.SubElement(file_node, "path")
                    path.text = path_formated



            #Création de la sous-node "deleted_files"
            if len(deleted_files) != 0:
                self.deleted_file_node = etree.SubElement(self.files_system_node, "deleted_file")

                #Création des sous-nodes fichiers supprimés
                for i in deleted_files:

                    name_formated = self.group_file_path(i)[0]
                    path_formated = self.group_file_path(i)[1]
                    
                    file_node = etree.SubElement(self.deleted_file_node, "file")
                    name = etree.SubElement(file_node, "name")
                    name.text = name_formated

                    path = etree.SubElement(file_node, "path")
                    path.text = path_formated


            #Création de la sous-node "modified_files"
            if len(modified_files) != 0:
                self.modified_file_node = etree.SubElement(self.files_system_node, "modified_file")

                #Création des sous-nodes fichiers modifiés
                for i in modified_files:

                    name_formated = self.group_file_path(i)[0]
                    path_formated = self.group_file_path(i)[1]
                    
                    file_node = etree.SubElement(self.modified_file_node, "file")
                    name = etree.SubElement(file_node, "name")
                    name.text = name_formated

                    path = etree.SubElement(file_node, "path")
                    path.text = path_formated


    def create_registry_modification_node(self, registry_file_path, registry_comparator_obj):

        created_path = registry_comparator_obj.created_path
        deleted_path = registry_comparator_obj.deleted_path
        created_keys = registry_comparator_obj.created_keys
        deleted_keys = registry_comparator_obj.deleted_keys
        modified_keys = registry_comparator_obj.modified_keys
        
        #Création de la node files_system
        if self.registry_modification_node is None:
            self.registry_modification_node = etree.SubElement(self.analysis_node, "registry_modification")

        file_node = etree.SubElement(self.registry_modification_node, "registry_file")

        path_file_node = etree.SubElement(file_node, "file_path")
        path_file_node.text = registry_file_path

        #création de la node path_modification
        if len(created_path) != 0 or len(deleted_path) != 0:
            path_modification_node = etree.SubElement(file_node, "path_modification")

            if len(created_path) != 0:
                added_path_node = etree.SubElement(path_modification_node, "added_paths")

                for i in created_path:
                    path_node = etree.SubElement(added_path_node, "path")
                    path_node.text = i

            if len(deleted_path) != 0:
                deleted_path_node = etree.SubElement(path_modification_node, "deleted_paths")

                for i in deleted_path:
                    path_node = etree.SubElement(deleted_path_node, "path")
                    path_node.text = i

        #création de la node key_modification
        if len(created_keys) != 0 or len(deleted_keys) != 0 or len(modified_keys) != 0:
           key_modification_node = etree.SubElement(file_node, "key_modification")

           if len(created_keys) != 0:
                added_keys_node = etree.SubElement(key_modification_node, "added_keys")

                for i in created_keys:
                    key_node = etree.SubElement(added_keys_node, "key")
                    path_node = etree.SubElement(key_node, "key_path")
                    path_node.text = i[0]
                    name_node = etree.SubElement(key_node, "name")
                    name_node.text = i[1]
                    value_node = etree.SubElement(key_node, "value")
                    value_node.text = i[2]
                    type_node = etree.SubElement(key_node, "type")
                    type_node.text = i[3]

           if len(deleted_keys) != 0:
                deleted_keys_node = etree.SubElement(key_modification_node, "deleted_keys")

                for i in deleted_keys:
                    key_node = etree.SubElement(deleted_keys_node, "key")
                    path_node = etree.SubElement(key_node, "key_path")
                    path_node.text = i[0]
                    name_node = etree.SubElement(key_node, "name")
                    name_node.text = i[1]
                    value_node = etree.SubElement(key_node, "value")
                    value_node.text = i[2]
                    type_node = etree.SubElement(key_node, "type")
                    type_node.text = i[3]

           if len(modified_keys) != 0:
                modified_keys_node = etree.SubElement(key_modification_node, "modified_keys")

                for i in modified_keys:
                    key_node = etree.SubElement(modified_keys_node, "key")
                    path_node = etree.SubElement(key_node, "key_path")
                    path_node.text = i[0]
                    name_node = etree.SubElement(key_node, "name")
                    name_node.text = i[1]
                    old_value_node = etree.SubElement(key_node, "old_value")
                    old_value_node.text = i[2]
                    new_value_node = etree.SubElement(key_node, "new_value")
                    new_value_node.text = i[3]
                    type_node = etree.SubElement(key_node, "type")
                    type_node.text = i[4]



    def create_log_modification_node(self, pathFile, addedNodes):
        
        if self.log_added_event is None:
            self.log_added_event = etree.SubElement(self.analysis_node, "logs_modification")

        if len(addedNodes) > 0:
            log_file_node = etree.SubElement(self.log_added_event, "logs_file")
            path_node  = etree.SubElement(log_file_node, "path")
            path_node.text = pathFile
            added_events_node  = etree.SubElement(log_file_node, "added_events")

                 
            for event_node in addedNodes:
                added_events_node.append(event_node)
                            
    def group_file_path(self, string):

        if string is not None:
            group_string = string.split("/")
            name = ""
            path = ""

            #le nom correspond au dernier groupe du split
            if len(group_string) > 0:
                name = group_string[len(group_string)-1]

                #si fichier placé à la racine
                if len(group_string) == 2 and group_string[0] == "":
                    path = "/" 

                #si fichier présent dans un répertoire
                elif len(group_string) > 1:
                    for i in range(0, len(group_string)-2):
                        path += "/" + group_string[i]
                    path += "/"

            string_formated = [name, path]
            return string_formated

        return 0
            

                
                

    
