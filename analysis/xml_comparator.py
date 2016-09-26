#!/usr/local/bin/python3.5

from lxml import etree

class XmlComparator:

    #File System data
    added_files_new = []
    added_files_missing = []

    deleted_files_new = []
    deleted_files_missing = []

    modified_files_new = []
    modified_files_missing = []

    #registry data
    reg_added_path_new = {}
    reg_deleted_path_new = {}
    reg_added_path_missing = {}
    reg_deleted_path_missing = {}

    reg_added_keys_new = {}
    reg_deleted_keys_new = {}
    reg_modified_keys_new = {}

    reg_added_keys_missing = {}
    reg_deleted_keys_missing = {}
    reg_modified_keys_missing = {}

    reg_added_keys_changing_ref = {}
    reg_deleted_keys_changing_ref = {}
    reg_modified_keys_changing_ref = {}

    reg_added_keys_changing_sample = {}
    reg_deleted_keys_changing_sample = {}
    reg_modified_keys_changing_sample = {}

    #logs file data
    added_event_new = {}
    added_event_missing = {}
    added_event_modified_ref = {}
    added_event_modified_sample = {}

    
    def __init__(self, path_ref, path_sample):

        #Node XML
        self.xml_ref_path = path_ref
        self.xml_sample_path = path_sample
        self.ref_tree = etree.parse(self.xml_ref_path)
        self.sample_tree = etree.parse(self.xml_sample_path)
        

        added_files_new = []
        added_files_missing = []

        deleted_files_new = []
        deleted_files_missing = []
        
        modified_files_new = []
        modified_files_missing = []


    def compare_xml(self):
        
        self.compare_file_system_added_file()
        self.compare_file_system_deleted_file()
        self.compare_file_system_modified_file()

        self.compare_registry()

        self.compare_logs()
        

    def compare_file_system_added_file(self):

        # File system comparaison
        if self.ref_tree.xpath("/analysis/files_system/added_file/file") != self.sample_tree.xpath("/analysis/files_system/added_file/file"):

            # On parcourt la référence pour trouver les fichier ajouté dans la référence et non ajouté dans l'echantillon analysé
            for i in self.ref_tree.xpath("/analysis/files_system/added_file/file"):
                
                present = False

                for j in self.sample_tree.xpath("/analysis/files_system/added_file/file"):

                    if (i.find("name").text == j.find("name").text and i.find("path").text == j.find("path").text):                        
                        present = True
                        break

                if present == False:
                    self.added_files_missing.append(i)



            # On parcourt la référence pour trouver les fichier ajouté dans  l'echantillon analysé et non ajouté dans la référence
            for i in self.sample_tree.xpath("/analysis/files_system/added_file/file"):
                
                present = False

                for j in self.ref_tree.xpath("/analysis/files_system/added_file/file"):

                    if (i.find("name").text == j.find("name").text and i.find("path").text == j.find("path").text):                           
                        present = True
                        break

                if present == False:
                    self.added_files_new.append(i)

                    
    def compare_file_system_deleted_file(self):

        # File system comparaison
        if self.ref_tree.xpath("/analysis/files_system/deleted_file/file") != self.sample_tree.xpath("/analysis/files_system/deleted_file/file"):

            # On parcourt la référence pour trouver les fichier supprimé dans la référence et non supprimé dans l'echantillon analysé
            for i in self.ref_tree.xpath("/analysis/files_system/deleted_file/file"):
                
                present = False

                for j in self.sample_tree.xpath("/analysis/files_system/deleted_file/file"):

                    if (i.find("name").text == j.find("name").text and i.find("path").text == j.find("path").text):                           
                        present = True
                        break

                if present == False:
                    self.deleted_files_missing.append(i)



            # On parcourt la référence pour trouver les fichier supprimé dans  l'echantillon analysé et non supprimé dans la référence
            for i in self.sample_tree.xpath("/analysis/files_system/deleted_file/file"):
                
                present = False

                for j in self.ref_tree.xpath("/analysis/files_system/deleted_file/file"):

                    if (i.find("name").text == j.find("name").text and i.find("path").text == j.find("path").text):                            
                        present = True
                        break

                if present == False:
                    self.deleted_files_new.append(i)

                    
    def compare_file_system_modified_file(self):

        # File system comparaison
        if self.ref_tree.xpath("/analysis/files_system/modified_file/file") != self.sample_tree.xpath("/analysis/files_system/modified_file/file"):

            # On parcourt la référence pour trouver les fichier modifié dans la référence et non modifié dans l'echantillon analysé
            for i in self.ref_tree.xpath("/analysis/files_system/modified_file/file"):
                
                present = False

                for j in self.sample_tree.xpath("/analysis/files_system/modified_file/file"):

                    if (i.find("name").text == j.find("name").text and i.find("path").text == j.find("path").text):                           
                        present = True
                        break

                if present == False:
                    self.modified_files_missing.append(i)



            # On parcourt la référence pour trouver les fichier modifié dans l'echantillon analysé et non modifié dans la référence
            for i in self.sample_tree.xpath("/analysis/files_system/modified_file/file"):
                
                present = False

                for j in self.ref_tree.xpath("/analysis/files_system/modified_file/file"):

                    if (i.find("name").text == j.find("name").text and i.find("path").text == j.find("path").text):                           
                        present = True
                        break

                if present == False:
                    self.modified_files_new.append(i)











                    
                
    def compare_registry(self):

        ref_added_path = {}
        ref_deleted_path = {}
        ref_added_keys = {}
        ref_deleted_keys = {}
        ref_modified_keys = {}

        sample_added_path = {}
        sample_deleted_path = {}
        sample_added_keys = {}
        sample_deleted_keys = {}
        sample_modified_keys = {}

        ##################################################################
        # recupération des données nécessaire à la comparaison ###########
        ##################################################################

        for registry_file in self.ref_tree.xpath("/analysis/registry_modification/registry_file"):            
            file_path = ""

            for children in registry_file.getchildren():

                #Path du fichier registre
                if children.tag == "file_path":
                    file_path = children.text

                # Modification des paths
                if children.tag == "path_modification":
                    for paths in children.getchildren():
                        if paths.tag == "added_paths":
                            ref_added_path[file_path] = []
                            ref_added_path[file_path] += paths.getchildren()

                        elif paths.tag == "deleted_paths":
                            ref_deleted_path[file_path] = []
                            ref_deleted_path[file_path] += paths.getchildren()

                # Modification des clées
                if children.tag == "key_modification":
                    for keys in children.getchildren():
                        if keys.tag == "added_keys":
                            ref_added_keys[file_path] = []
                            ref_added_keys[file_path] += keys.getchildren()

                        elif keys.tag == "deleted_keys":
                            ref_deleted_keys[file_path] = []
                            ref_deleted_keys[file_path] += keys.getchildren()

                        elif keys.tag == "modified_keys":
                            ref_modified_keys[file_path] = []
                            ref_modified_keys[file_path] += keys.getchildren()


        for registry_file in self.sample_tree.xpath("/analysis/registry_modification/registry_file"):
            
            file_path = ""

            for children in registry_file.getchildren():

                #Path du fichier registre
                if children.tag == "file_path":
                    file_path = children.text

                # Modification des paths
                if children.tag == "path_modification":
                    for paths in children.getchildren():
                        if paths.tag == "added_paths":
                            sample_added_path[file_path] = []
                            sample_added_path[file_path] += paths.getchildren()

                        elif paths.tag == "deleted_paths":
                            sample_deleted_path[file_path] = []
                            sample_deleted_path[file_path] += paths.getchildren()

                # Modification des clées
                if children.tag == "key_modification":
                    for keys in children.getchildren():
                        if keys.tag == "added_keys":
                            sample_added_keys[file_path] = []
                            sample_added_keys[file_path] += keys.getchildren()

                        elif keys.tag == "deleted_keys":
                            sample_deleted_keys[file_path] = []
                            sample_deleted_keys[file_path] += keys.getchildren()

                        elif keys.tag == "modified_keys":
                            sample_modified_keys[file_path] = []
                            sample_modified_keys[file_path] += keys.getchildren()

                
                            
        ##################################################################
        # Comparasion reference/resultat des données receuillies - PATH###
        ##################################################################
        
        # Comparaison pour trouver les paths ajouté manquant dans l'extrait analysé
        for registry_path in ref_added_path.keys():
            self.reg_added_path_missing[registry_path] = []
            for ref_path in ref_added_path[registry_path]:                
                present = False
                
                if registry_path in sample_added_path:
                    for sample_path in sample_added_path[registry_path]:
                        if sample_path.text == ref_path.text:
                            present = True

                    if present == False:
                        self.reg_added_path_missing[registry_path].append(ref_path)

                else:
                    self.reg_added_path_missing[registry_path].append(ref_path)


        # Comparaison pour trouver les paths ajouté en plus dans l'extrait analysé
        for registry_path in sample_added_path.keys():
            self.reg_added_path_new[registry_path] = []
            
            for sample_path in sample_added_path[registry_path]:                
                present = False
                
                if registry_path in ref_added_path:
                    for ref_path in ref_added_path[registry_path]:
                        if ref_path.text == sample_path.text:
                            present = True

                    if present == False:
                        self.reg_added_path_new[registry_path].append(sample_path)

                else:
                    self.reg_added_path_new[registry_path].append(sample_path)


        # Comparaison pour trouver les paths supprimé manquant dans l'extrait analysé
        for registry_path in ref_deleted_path.keys():
            self.reg_deleted_path_missing[registry_path] = []
            
            for ref_path in ref_deleted_path[registry_path]:                
                present = False
                
                if registry_path in sample_deleted_path:
                    for sample_path in sample_deleted_path[registry_path]:
                        if sample_path.text == ref_path.text:
                            present = True

                    if present == False:
                        self.reg_deleted_path_missing[registry_path].append(ref_path)

                else:
                    self.reg_deleted_path_missing[registry_path].append(ref_path)
                    

        # Comparaison pour trouver les paths supprimé en plus dans l'extrait analysé
        for registry_path in sample_deleted_path.keys():
            self.reg_deleted_path_new[registry_path] = []
            
            for sample_path in sample_deleted_path[registry_path]:                
                present = False
                
                if registry_path in ref_deleted_path:
                    for ref_path in ref_deleted_path[registry_path]:
                        if ref_path.text == sample_path.text:
                            present = True

                    if present == False:
                        self.reg_deleted_path_new[registry_path].append(sample_path)

                else:
                    self.reg_deleted_path_new[registry_path].append(sample_path)







                    
        ##################################################################
        # Comparasion reference/resultat des données receuillies - KEY ###
        ##################################################################
        
        # Comparaison pour trouver les clé de registres ajoutées manquant dans l'extrait analysé
        for registry_path in ref_added_keys.keys():

            self.reg_added_keys_missing[registry_path] = []
            self.reg_added_keys_changing_ref[registry_path] = []            
            self.reg_added_keys_changing_sample[registry_path] = []
            
            for ref_key in ref_added_keys[registry_path]:
                present = False
                modified = False

                if registry_path in sample_added_keys:
                    for sample_key in sample_added_keys[registry_path]:

                        if (sample_key.find("key_path").text == ref_key.find("key_path").text and sample_key.find("name").text == ref_key.find("name").text and sample_key.find("type").text == ref_key.find("type").text):
                            present = True

                            if (sample_key.find("value").text != ref_key.find("value").text):
                                modified = True
                                self.reg_added_keys_changing_sample[registry_path].append(sample_key)

                    if modified == True:
                        self.reg_added_keys_changing_ref[registry_path].append(ref_key)
                        
                    elif present == False:
                        self.reg_added_keys_missing[registry_path].append(ref_key)

                else:
                    self.reg_added_keys_missing[registry_path].append(ref_key)



        # Comparaison pour trouver les clé de registres ajoutées en plus dans l'extrait analysé
        for registry_path in sample_added_keys.keys():
            self.reg_added_keys_new[registry_path] = []
            
            for sample_key in sample_added_keys[registry_path]:                
                present = False

                if registry_path in ref_added_keys:
                    for ref_key in ref_added_keys[registry_path]:

                        if (ref_key.find("key_path").text == sample_key.find("key_path").text and ref_key.find("name").text == sample_key.find("name").text and ref_key.find("type").text == sample_key.find("type").text):
                            present = True

                    if present == False:
                        self.reg_added_keys_new[registry_path].append(sample_key)
                else:
                    self.reg_added_keys_new[registry_path].append(sample_key)


        # Comparaison pour trouver les clé de registres supprimées manquantes dans l'extrait analysé
        for registry_path in ref_deleted_keys.keys():

            self.reg_deleted_keys_missing[registry_path] = []
            self.reg_deleted_keys_changing_ref[registry_path] = []
            self.reg_deleted_keys_changing_sample[registry_path] = []
            
            for ref_key in ref_deleted_keys[registry_path]:
                present = False
                modified = False

                if registry_path in sample_deleted_keys:
                    for sample_key in sample_deleted_keys[registry_path]:

                        if (sample_key.find("key_path").text == ref_key.find("key_path").text and sample_key.find("name").text == ref_key.find("name").text and sample_key.find("type").text == ref_key.find("type").text):
                            present = True

                            if (sample_key.find("value").text != ref_key.find("value").text):
                                modified = True                                
                                self.reg_deleted_keys_changing_sample[registry_path].append(sample_key)

                    if modified == True:
                        self.reg_deleted_keys_changing_ref[registry_path].append(ref_key)
                        
                    elif present == False:
                        self.reg_deleted_keys_missing[registry_path].append(ref_key)

                else:
                    self.reg_deleted_keys_missing[registry_path].append(ref_key)



        # Comparaison pour trouver les clé de registres supprimées en plus dans l'extrait analysé
        for registry_path in sample_deleted_keys.keys():
            self.reg_deleted_keys_new[registry_path] = []
            
            for sample_key in sample_deleted_keys[registry_path]:                
                present = False

                if registry_path in ref_deleted_keys:
                    for ref_key in ref_deleted_keys[registry_path]:

                        if (ref_key.find("key_path").text == sample_key.find("key_path").text and ref_key.find("name").text == sample_key.find("name").text and ref_key.find("type").text == sample_key.find("type").text):
                            present = True

                    if present == False:
                        self.reg_deleted_keys_new[registry_path].append(sample_key)
                else:
                    self.reg_deleted_keys_new[registry_path].append(sample_key)







        # Comparaison pour trouver les clé de registres modifiés manquantes dans l'extrait analysé
        for registry_path in ref_modified_keys.keys():

            self.reg_modified_keys_missing[registry_path] = []
            self.reg_modified_keys_changing_ref[registry_path] = []
            self.reg_modified_keys_changing_sample[registry_path] = []
            
            for ref_key in ref_modified_keys[registry_path]:
                present = False
                modified = False

                if registry_path in sample_modified_keys:
                    for sample_key in sample_modified_keys[registry_path]:

                        if (sample_key.find("key_path").text == ref_key.find("key_path").text and sample_key.find("name").text == ref_key.find("name").text and sample_key.find("type").text == ref_key.find("type").text):
                            present = True

                            if (sample_key.find("old_value").text != ref_key.find("old_value").text or sample_key.find("new_value").text != ref_key.find("new_value").text):
                                modified = True                                
                                self.reg_modified_keys_changing_sample[registry_path].append(sample_key)

                    if modified == True:
                        self.reg_modified_keys_changing_ref[registry_path].append(ref_key)
                        
                    elif present == False:
                        self.reg_modified_keys_missing[registry_path].append(ref_key)

                else:
                    self.reg_modified_keys_missing[registry_path].append(ref_key)



        # Comparaison pour trouver les clé de registres modifiées en plus dans l'extrait analysé
        for registry_path in sample_modified_keys.keys():
            self.reg_modified_keys_new[registry_path] = []
            
            for sample_key in sample_modified_keys[registry_path]:                
                present = False

                if registry_path in ref_modified_keys:
                    for ref_key in ref_modified_keys[registry_path]:

                        if (ref_key.find("key_path").text == sample_key.find("key_path").text and ref_key.find("name").text == sample_key.find("name").text and ref_key.find("type").text == sample_key.find("type").text):
                            present = True

                    if present == False:
                        self.reg_modified_keys_new[registry_path].append(sample_key)
                else:
                    self.reg_modified_keys_new[registry_path].append(sample_key)   




    def compare_logs(self):

        ref_added_event = {}
        sample_added_event = {}

        #Récupération des évent créé pour la référence
        for logs_file in self.ref_tree.xpath("/analysis/logs_modification/logs_file"):            
            file_path = ""

            for children in logs_file.getchildren():

                #Path du fichier logs
                if children.tag == "path":
                    file_path = children.text

                # listing des events
                if children.tag == "added_events":
                    ref_added_event[file_path] = []
                    for event in children.getchildren():
                        ref_added_event[file_path].append(event)


        #Récupération des évent créé pour l'échantillon
        for logs_file in self.sample_tree.xpath("/analysis/logs_modification/logs_file"):            
            file_path = ""

            for children in logs_file.getchildren():

                #Path du fichier logs
                if children.tag == "path":
                    file_path = children.text

                # listing des events
                if children.tag == "added_events":
                    sample_added_event[file_path] = []
                    for event in children.getchildren():
                        sample_added_event[file_path].append(event)



        #comparaison
        for logs_path in ref_added_event.keys():
            self.added_event_missing[logs_path] = []
            self.added_event_modified_sample[logs_path] = []            
            self.added_event_modified_ref[logs_path] = []

            for event_ref in ref_added_event[logs_path]:
                present = False
                modified = False

                if logs_path in sample_added_event:
                    for event_sample in sample_added_event[logs_path]:                        

                        if(event_ref.find("System/EventRecordID").text == event_sample.find("System/EventRecordID").text and event_ref.find("System/EventID").text == event_sample.find("System/EventID").text and event_ref.find("System/Level").text == event_sample.find("System/Level").text and event_ref.find("System/Keywords").text == event_sample.find("System/Keywords").text):
                            present = True

                            if (event_ref.xpath("EventData/Data") is not None):
                                if (len(event_ref.xpath("EventData/Data")) == len(event_sample.xpath("EventData/Data"))):
                                    data_ref = event_ref.xpath("EventData/Data")
                                    data_sample = event_sample.xpath("EventData/Data")                                
                                
                                    for i in range(0, len(data_ref)):
                                        if data_ref[i].text != data_sample[i].text:
                                            modified = True
                                            self.added_event_modified_sample[logs_path].append(event_sample)
                                            break
                                            
                                else:
                                    modified = True
                                    self.added_event_modified_sample[logs_path].append(event_sample)

                    if modified == True:
                        self.added_event_modified_ref[logs_path].append(event_ref)
                    if present == False:
                        self.added_event_missing[logs_path].append(event_ref)

                else:
                     self.added_event_missing[logs_path].append(event_ref)



                    
        # comparaison logs en plus que la référence
        for logs_path in sample_added_event.keys():
            self.added_event_new[logs_path] = []

            for event_sample in sample_added_event[logs_path]:
                present = False

                if logs_path in ref_added_event:
                    for event_ref in ref_added_event[logs_path]:                        

                        if(event_sample.find("System/EventRecordID").text == event_ref.find("System/EventRecordID").text and event_sample.find("System/EventID").text == event_ref.find("System/EventID").text and event_sample.find("System/Level").text == event_ref.find("System/Level").text and event_sample.find("System/Keywords").text == event_ref.find("System/Keywords").text):
                            present = True

                           
                    if present == False:
                        self.added_event_new[logs_path].append(event_sample)

                else:
                     self.added_event_new[logs_path].append(event_sample)





    def print_results(self):

        print("###############################################################################")
        print("                "+self.xml_ref_path.split('/')[-1]+"                           ")
        print("################################################# #############################")
        

        print("Ce fichier decrit les differences entre le comportement normal de l'executable qui correspond au fichier xml stocke dans \"results/references_xml\" et du resultat de l'analyse precedente stockee dans \"results/xml_result\". L'echantillon represente ici le système de fichier analyses, la reference represente le système de fichier d'un comportement normal de l'executable: \n \n")
        
        print("############################# File System Changes #############################")
        print("Fichiers crees à l'execution\n")
        if self.added_files_new is not None:
            print("Les fichiers suivants ont ete crees dans l'echantillon et n'etaient pas present dans la reference:")
            for i in self.added_files_new:
                print(i.find("path").text+i.find("name").text)
            print("")

        if self.added_files_missing is not None:
            print("Les fichiers suivants ont ete crees dans la reference et n'etaient pas present dans l'echantillon:")
            for i in self.added_files_missing:
                print(i.find("path").text+i.find("name").text)
            print("\n")

        print("Fichiers supprimes à l'execution\n")
        if self.deleted_files_new is not None:
            print("Les fichiers suivants ont ete supprimes dans l'echantillon et n'etaient pas supprimes dans la reference:")
            for i in self.deleted_files_new:
                print(i.find("path").text+i.find("name").text)
            print("")

        if self.deleted_files_missing is not None:
            print("Les fichiers suivants ont ete supprimes dans la reference et n'etaient pas supprimes dans l'echantillon:")
            for i in self.deleted_files_missing:
                print(i.find("path").text+i.find("name").text)
            print("\n")

        print("Fichiers modifies à l'execution\n")
        if self.modified_files_new is not None:
            print("Les fichiers suivants ont ete modifies dans l'echantillon et n'etaient pas modifies dans la reference:")
            for i in self.modified_files_new:
                print(i.find("path").text+i.find("name").text)
            print("")

        if self.modified_files_missing is not None:
            print("Les fichiers suivants ont ete modifies dans la reference et n'etaient pas modifies dans l'echantillon:")
            for i in self.modified_files_missing:
                print(i.find("path").text+i.find("name").text)
            print("\n")


            
        print("############################# Registry Files Changes #############################")
        print("Changements au niveau du path des registres:\n")
        if self.reg_added_path_missing is not None:
            print("Les paths suivants ont ete crees dans la reference et n'etaient pas crees dans l'echantillon:")
            for reg in self.reg_added_path_missing.keys():
                print("Dans le registre "+reg+":")

                for path in self.reg_added_path_missing[reg]:
                    print(path.text)
                print("")
        
        if self.reg_added_path_new is not None:
            print("Les paths suivants ont ete crees dans l'echantillon et n'etaient pas crees dans la reference:")
            for reg in self.reg_added_path_new.keys():
                print("Dans le registre "+reg+":")

                for path in self.reg_added_path_new[reg]:
                    print(path.text)
                print("")
            print("")

        if self.reg_deleted_path_missing is not None:
            print("Les paths suivants ont ete supprimes dans la reference et n'etaient pas supprimes dans l'echantillon:")
            for reg in self.reg_deleted_path_missing.keys():
                print("Dans le registre "+reg+":")

                for path in self.reg_deleted_path_missing[reg]:
                    print(path.text)
                print("")
        
        if self.reg_deleted_path_new is not None:
            print("Les paths suivants ont ete supprimes dans l'echantillon et n'etaient pas supprimes dans la reference:")
            for reg in self.reg_deleted_path_new.keys():
                print("Dans le registre "+reg+":")

                for path in self.reg_deleted_path_new[reg]:
                    print(path.text)
                print("")
            print("")



        print("Changements au niveau des cles des registres:\n")
        if self.reg_added_keys_missing is not None:
            print("Les clees de registres suivantes ont ete creees dans la reference et n'etaient pas creees dans l'echantillon:")
            for reg in self.reg_added_keys_missing.keys():
                if len(self.reg_added_keys_missing[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for key in self.reg_added_keys_missing[reg]:
                        print("Path: "+key.find("key_path").text)
                        print("Cle: "+key.find("name").text)
                        print("Valeur: "+key.find("value").text)
                        print("Type: "+key.find("type").text)
                        print("-----------------")
                    print("")

        if self.reg_added_keys_new is not None:
            print("Les clees de registres suivantes ont ete creees dans l'echantillon et n'etaient pas creees dans la reference:")
            for reg in self.reg_added_keys_new.keys():
                if len(self.reg_added_keys_new[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for key in self.reg_added_keys_new[reg]:
                        print("Path: "+key.find("key_path").text)
                        print("Cle: "+key.find("name").text)
                        print("Valeur: "+key.find("value").text)
                        print("Type: "+key.find("type").text)
                        print("-----------------")
                    print("")

        if self.reg_added_keys_changing_sample is not None:
            print("Les clees de registres suivantes ont ete creees dans l'echantillon ET dans la reference mais n'ont pas reçue la même valeur:")
            for reg in self.reg_added_keys_changing_sample.keys():
                if len(self.reg_added_keys_changing_sample[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for i in range(0, len(self.reg_added_keys_changing_ref[reg])):
                        key_1 = self.reg_added_keys_changing_ref[reg][i]
                        key_2 = self.reg_added_keys_changing_sample[reg][i]
                        print("Path: "+key_1.find("key_path").text)
                        print("Cle: "+key_1.find("name").text)
                        print("Valeur reference: "+key_1.find("value").text)
                        print("Valeur echantillon: "+key_2.find("value").text)
                        print("Type: "+key_1.find("type").text)
                        print("-----------------")
                    print("")







        if self.reg_deleted_keys_missing is not None:
            print("Les clees de registres suivantes ont ete supprimees dans la reference et n'etaient pas supprimees dans l'echantillon:")
            for reg in self.reg_deleted_keys_missing.keys():
                if len(self.reg_deleted_keys_missing[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for key in self.reg_deleted_keys_missing[reg]:
                        print("Path: "+key.find("key_path").text)
                        print("Cle: "+key.find("name").text)
                        print("Valeur: "+key.find("value").text)
                        print("Type: "+key.find("type").text)
                        print("-----------------")
                    print("")

        if self.reg_deleted_keys_new is not None:
            print("Les clees de registres suivantes ont ete supprimees dans l'echantillon et n'etaient pas supprimees dans la reference:")
            for reg in self.reg_deleted_keys_new.keys():
                if len(self.reg_deleted_keys_new[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for key in self.reg_deleted_keys_new[reg]:
                        print("Path: "+key.find("key_path").text)
                        print("Cle: "+key.find("name").text)
                        print("Valeur: "+key.find("value").text)
                        print("Type: "+key.find("type").text)
                        print("-----------------")
                    print("")

        if self.reg_deleted_keys_changing_sample is not None:
            print("Les clees de registres suivantes ont ete supprimees dans l'echantillon ET dans la reference mais n'avaient pas la même valeur initiale:")
            for reg in self.reg_deleted_keys_changing_sample.keys():
                if len(self.reg_deleted_keys_changing_sample[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for i in range(0, len(self.reg_deleted_keys_changing_ref[reg])):
                        key_1 = self.reg_deleted_keys_changing_ref[reg][i]
                        key_2 = self.reg_deleted_keys_changing_sample[reg][i]
                        print("Path: "+key_1.find("key_path").text)
                        print("Cle: "+key_1.find("name").text)
                        print("Valeur reference: "+key_1.find("value").text)
                        print("Valeur echantillon: "+key_2.find("value").text)
                        print("Type: "+key_1.find("type").text)
                        print("-----------------")
                    print("")






        if self.reg_modified_keys_missing is not None:
            print("Les clees de registres suivantes ont ete modifiees dans la reference et n'etaient pas modifiees dans l'echantillon:")
            for reg in self.reg_modified_keys_missing.keys():
                if len(self.reg_modified_keys_missing[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for key in self.reg_modified_keys_missing[reg]:
                        print("Path: "+key.find("key_path").text)
                        print("Cle: "+key.find("name").text)
                        print("Valeur avant execution: "+key.find("old_value").text)
                        print("Valeur apres execution: "+key.find("new_value").text)
                        print("Type: "+key.find("type").text)
                        print("-----------------")
                    print("")

        if self.reg_modified_keys_new is not None:
            print("Les clees de registres suivantes ont ete modifiees dans l'echantillon et n'etaient pas modifiees dans la reference:")
            for reg in self.reg_modified_keys_new.keys():
                if len(self.reg_modified_keys_new[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for key in self.reg_modified_keys_new[reg]:
                        print("Path: "+key.find("key_path").text)
                        print("Cle: "+key.find("name").text)
                        print("Valeur avant execution: "+key.find("old_value").text)
                        print("Valeur apres execution: "+key.find("new_value").text)
                        print("Type: "+key.find("type").text)
                        print("-----------------")
                    print("")

        if self.reg_modified_keys_changing_sample is not None:
            print("Les clees de registres suivantes ont ete modifiees dans l'echantillon ET dans la reference mais n'ont pas reçue la même valeur:")
            for reg in self.reg_modified_keys_changing_sample.keys():
                if len(self.reg_modified_keys_changing_sample[reg]) > 0:
                    print("Dans le registre "+reg+":")

                    for i in range(0, len(self.reg_modified_keys_changing_ref[reg])):
                        key_1 = self.reg_modified_keys_changing_ref[reg][i]
                        key_2 = self.reg_modified_keys_changing_sample[reg][i]
                        print("Path: "+key_1.find("key_path").text)
                        print("Cle: "+key_1.find("name").text)
                        print("Valeur initiale reference : "+key_1.find("old_value").text)
                        print("Valeur initiale echantillon: "+key_2.find("old_value").text)
                        print("Valeur finale reference: "+key_1.find("new_value").text)
                        print("Valeur finaleechantillon: "+key_2.find("new_value").text)
                        print("Type: "+key_1.find("type").text)
                        print("-----------------")
                    print("")






        print("############################# Logs Files Changes #############################")
        print("Changements au niveau des logs:\n")
        if self.added_event_missing is not None:
            print("Les logs suivants ont ete ajoutes dans la reference et n'etaient pas ajoutes dans l'echantillon:")
            for log in self.added_event_missing.keys():
                if len(self.added_event_missing[log]) > 0:
                    print("Dans le journal d'evenements "+log+":")

                    for event in self.added_event_missing[log]:
                        for child in event.find("System"):
                            print(str(child.tag)+": "+str(child.text))
                        for child in event.find("EventData"):
                            print(str(child.tag)+": "+str(child.text))
                        print("-----------------")
                    print("")


        if self.added_event_new is not None:
            print("Les logs suivants ont ete ajoutes dans l'echantillon et n'etaient pas ajoutes dans la reference:")
            for log in self.added_event_new.keys():
                if len(self.added_event_new[log]) > 0:
                    print("Dans le journal d'evenements "+log+":")

                    for event in self.added_event_new[log]:
                        for child in event.find("System"):
                            print(str(child.tag)+": "+str(child.text))
                        for child in event.find("EventData"):
                            print(str(child.tag)+": "+str(child.text))
                        print("-----------------")
                    print("")

        if self.added_event_modified_ref is not None:
            print("Les logs suivants ont ete ajoutes dans l'echantillon ET dans la reference mais n'ont pas ete crees identiquement:")
            for log in self.added_event_modified_ref.keys():
                if len(self.added_event_modified_ref[log]) > 0:
                    print("Dans le journal d'evenements "+log+":")

                    for i in range(0, len(self.added_event_modified_ref[log])):
                        event_1 = self.added_event_modified_ref[log][i]
                        event_2 = self.added_event_modified_sample[log][i]

                        print("Log reference:")
                        for child in event_1.find("System"):
                            print(str(child.tag)+": "+str(child.text))
                        for child in event_1.find("EventData"):
                            print(str(child.tag)+": "+str(child.text))
                        print("")
                        print("Log echantillon:")
                        for child in event_2.find("System"):
                            print(str(child.tag)+": "+str(child.text))
                        for child in event_2.find("EventData"):
                            print(str(child.tag)+": "+str(child.text))
                        print("-----------------")
                    print("")


    def create_result_file(self):

        output = ""

        output += "<b>###############################################################################</b></br>"
        output += "                "+self.xml_ref_path.split('/')[-1]+"                           </br>"
        output += "<b>################################################# #############################</b></br>"
        

        output += "Ce fichier decrit les différences entre le comportement normal de l'exécutable qui correspond au fichier xml stocké dans \"results/references_xml\" et du résultat de l'analyse précédente stockée dans \"results/xml_result\". L'échantillon représente ici le système de fichier analysés, la référence représente le système de fichier d'un comportement normal de l'exécutable: </br> </br></br>"
        
        output += "<b>############################# File System Changes #############################</b></br>"
        output += "<b>Fichiers créés à l'exécution</b></br></br>"
        if self.added_files_new is not None:
            output += "<u>Les fichiers suivants ont été créés dans l'échantillon et n'étaient pas présent dans la référence:</u></br>"
            for i in self.added_files_new:
                output += i.find("path").text+i.find("name").text+"</br>"
            output += "</br>"

        if self.added_files_missing is not None:
            output += "<u>Les fichiers suivants ont été créés dans la référence et n'étaient pas présent dans l'échantillon:</u></br>"
            for i in self.added_files_missing:
                output += i.find("path").text+i.find("name").text+"</br>"
            output += "</br></br>"

        output += "<b>Fichiers supprimés à l'exécution</b></br>"
        if self.deleted_files_new is not None:
            output += "<u>Les fichiers suivants ont été supprimés dans l'échantillon et n'étaient pas supprimés dans la référence:</u></br>"
            for i in self.deleted_files_new:
                output += i.find("path").text+i.find("name").text+"</br>"
            output += "</br>"

        if self.deleted_files_missing is not None:
            output += "<u>Les fichiers suivants ont été supprimés dans la référence et n'étaient pas supprimés dans l'échantillon:</u></br>"
            for i in self.deleted_files_missing:
                output += i.find("path").text+i.find("name").text+"</br>"
            output += "</br></br>"

        output += "<b>Fichiers modifiés à l'exécution</b></br>"
        if self.modified_files_new is not None:
            output += "<u>Les fichiers suivants ont été modifiés dans l'échantillon et n'étaient pas modifiés dans la référence:</u></br>"
            for i in self.modified_files_new:
                output += i.find("path").text+i.find("name").text+"</br>"
            output += "</br>"

        if self.modified_files_missing is not None:
            output += "<u>Les fichiers suivants ont été modifiés dans la référence et n'étaient pas modifiés dans l'échantillon:</u></br>"
            for i in self.modified_files_missing:
                output += i.find("path").text+i.find("name").text+"</br>"
            output += "</br></br>"


            
        output += "<b>############################# Registry Files Changes #############################</b></br>"
        output += "<b>Changements au niveau du path des registres:</b></br></br>"
        if self.reg_added_path_missing is not None:
            output += "<u>Les paths suivants ont été créés dans la référence et n'étaient pas créés dans l'échantillon:</u></br>"
            for reg in self.reg_added_path_missing.keys():
                output += "### Dans le registre "+reg+":</br>"

                for path in self.reg_added_path_missing[reg]:
                    output += path.text+"</br>"
                output += "</br>"
        
        if self.reg_added_path_new is not None:
            output += "<u>Les paths suivants ont été créés dans l'échantillon et n'étaient pas créés dans la référence:</u></br>"
            for reg in self.reg_added_path_new.keys():
                output += "### Dans le registre "+reg+":</br>"

                for path in self.reg_added_path_new[reg]:
                    output += path.text+"</br>"
                output += "</br>"
            output += "</br>"

        if self.reg_deleted_path_missing is not None:
            output += "<u>Les paths suivants ont été supprimés dans la référence et n'étaient pas supprimés dans l'échantillon:</u></br>"
            for reg in self.reg_deleted_path_missing.keys():
                output += "### Dans le registre "+reg+":</br>"

                for path in self.reg_deleted_path_missing[reg]:
                    output += path.text+"</br>"
                output += "</br>"
        
        if self.reg_deleted_path_new is not None:
            output += "<u>Les paths suivants ont été supprimés dans l'échantillon et n'étaient pas supprimés dans la référence:</u></br>"
            for reg in self.reg_deleted_path_new.keys():
                output += "### Dans le registre "+reg+":</br>"

                for path in self.reg_deleted_path_new[reg]:
                    output += path.text+"</br>"
                output += "</br>"
            output += "</br>"



        output += "<b>Changements au niveau des clés des registres:</b></br></br>"
        if self.reg_added_keys_missing is not None:
            output += "<u>Les clées de registres suivantes ont été créées dans la référence et n'étaient pas créées dans l'échantillon:</u></br>"
            for reg in self.reg_added_keys_missing.keys():
                if len(self.reg_added_keys_missing[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for key in self.reg_added_keys_missing[reg]:
                        output += "Path: "+key.find("key_path").text+"</br>"
                        output += "Clé: "+key.find("name").text+"</br>"
                        output += "Valeur: "+key.find("value").text+"</br>"
                        output += "Type: "+key.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"

        if self.reg_added_keys_new is not None:
            output += "<u>Les clées de registres suivantes ont été créées dans l'échantillon et n'étaient pas créées dans la référence:</u></br>"
            for reg in self.reg_added_keys_new.keys():
                if len(self.reg_added_keys_new[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for key in self.reg_added_keys_new[reg]:
                        output += "Path: "+key.find("key_path").text+"</br>"
                        output += "Clé: "+key.find("name").text+"</br>"
                        output += "Valeur: "+key.find("value").text+"</br>"
                        output += "Type: "+key.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"

        if self.reg_added_keys_changing_sample is not None:
            output += "<u>Les clées de registres suivantes ont été créées dans l'échantillon ET dans la référence mais n'ont pas reçue la même valeur:</u></br>"
            for reg in self.reg_added_keys_changing_sample.keys():
                if len(self.reg_added_keys_changing_sample[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for i in range(0, len(self.reg_added_keys_changing_ref[reg])):
                        key_1 = self.reg_added_keys_changing_ref[reg][i]
                        key_2 = self.reg_added_keys_changing_sample[reg][i]
                        output += "Path: "+key_1.find("key_path").text
                        output += "Clé: "+key_1.find("name").text+"</br>"
                        output += "Valeur référence: "+key_1.find("value").text+"</br>"
                        output += "Valeur echantillon: "+key_2.find("value").text+"</br>"
                        output += "Type: "+key_1.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"







        if self.reg_deleted_keys_missing is not None:
            output += "<u>Les clées de registres suivantes ont été supprimées dans la référence et n'étaient pas supprimées dans l'échantillon:</u></br>"
            for reg in self.reg_deleted_keys_missing.keys():
                if len(self.reg_deleted_keys_missing[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for key in self.reg_deleted_keys_missing[reg]:
                        output += "Path: "+key.find("key_path").text+"</br>"
                        output += "Clé: "+key.find("name").text+"</br>"
                        output += "Valeur: "+key.find("value").text+"</br>"
                        output += "Type: "+key.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"

        if self.reg_deleted_keys_new is not None:
            output += "<u>Les clées de registres suivantes ont été supprimées dans l'échantillon et n'étaient pas supprimées dans la référence:</u></br>"
            for reg in self.reg_deleted_keys_new.keys():
                if len(self.reg_deleted_keys_new[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for key in self.reg_deleted_keys_new[reg]:
                        output += "Path: "+key.find("key_path").text+"</br>"
                        output += "Clé: "+key.find("name").text+"</br>"
                        output += "Valeur: "+key.find("value").text+"</br>"
                        output += "Type: "+key.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"

        if self.reg_deleted_keys_changing_sample is not None:
            output += "<u>Les clées de registres suivantes ont été supprimées dans l'échantillon ET dans la référence mais n'avaient pas la même valeur initiale:</u></br>"
            for reg in self.reg_deleted_keys_changing_sample.keys():
                if len(self.reg_deleted_keys_changing_sample[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for i in range(0, len(self.reg_deleted_keys_changing_ref[reg])):
                        key_1 = self.reg_deleted_keys_changing_ref[reg][i]
                        key_2 = self.reg_deleted_keys_changing_sample[reg][i]
                        output += "Path: "+key_1.find("key_path").text+"</br>"
                        output += "Clé: "+key_1.find("name").text+"</br>"
                        output += "Valeur référence: "+key_1.find("value").text+"</br>"
                        output += "Valeur echantillon: "+key_2.find("value").text+"</br>"
                        output += "Type: "+key_1.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"






        if self.reg_modified_keys_missing is not None:
            output += "<u>Les clées de registres suivantes ont été modifiées dans la référence et n'étaient pas modifiées dans l'échantillon:</u></br>"
            for reg in self.reg_modified_keys_missing.keys():
                if len(self.reg_modified_keys_missing[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for key in self.reg_modified_keys_missing[reg]:
                        output += "Path: "+key.find("key_path").text+"</br>"
                        output += "Clé: "+key.find("name").text+"</br>"
                        output += "Valeur avant execution: "+key.find("old_value").text+"</br>"
                        output += "Valeur apres execution: "+key.find("new_value").text+"</br>"
                        output += "Type: "+key.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"
                    
        if self.reg_modified_keys_new is not None:
            output += "<u>Les clées de registres suivantes ont été modifiées dans l'échantillon et n'étaient pas modifiées dans la référence:</u></br>"
            for reg in self.reg_modified_keys_new.keys():
                if len(self.reg_modified_keys_new[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for key in self.reg_modified_keys_new[reg]:
                        output += "Path: "+key.find("key_path").text+"</br>"
                        output += "Clé: "+key.find("name").text+"</br>"
                        output += "Valeur avant execution: "+key.find("old_value").text+"</br>"
                        output += "Valeur apres execution: "+key.find("new_value").text+"</br>"
                        output += "Type: "+key.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"

        if self.reg_modified_keys_changing_sample is not None:
            output += "<u>Les clées de registres suivantes ont été modifiées dans l'échantillon ET dans la référence mais n'ont pas reçue la même valeur:</u></br>"
            for reg in self.reg_modified_keys_changing_sample.keys():
                if len(self.reg_modified_keys_changing_sample[reg]) > 0:
                    output += "### Dans le registre "+reg+":</br>"

                    for i in range(0, len(self.reg_modified_keys_changing_ref[reg])):
                        key_1 = self.reg_modified_keys_changing_ref[reg][i]
                        key_2 = self.reg_modified_keys_changing_sample[reg][i]
                        output += "Path: "+key_1.find("key_path").text+"</br>"
                        output += "Clé: "+key_1.find("name").text+"</br>"
                        output += "Valeur initiale référence : "+key_1.find("old_value").text+"</br>"
                        output += "Valeur initiale echantillon: "+key_2.find("old_value").text+"</br>"
                        output += "Valeur finale référence: "+key_1.find("new_value").text+"</br>"
                        output += "Valeur finaleechantillon: "+key_2.find("new_value").text+"</br>"
                        output += "Type: "+key_1.find("type").text+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"






        output += "<b>############################# Logs Files Changes #############################</b></br>"
        output += "<b>Changements au niveau des logs:</b></br></br>"
        if self.added_event_missing is not None:
            output += "<u>Les logs suivants ont été ajoutés dans la référence et n'étaient pas ajoutés dans l'échantillon:</u></br>"
            for log in self.added_event_missing.keys():
                if len(self.added_event_missing[log]) > 0:
                    output += "### Dans le journal d'événements </br>"+log+":</br>"

                    for event in self.added_event_missing[log]:
                        for child in event.find("System"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        for child in event.find("EventData"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"


        if self.added_event_new is not None:
            output += "<u>Les logs suivants ont été ajoutés dans l'échantillon et n'étaient pas ajoutés dans la référence:</u></br>"
            for log in self.added_event_new.keys():
                if len(self.added_event_new[log]) > 0:
                    output += "### Dans le journal d'événements "+log+":</br>"

                    for event in self.added_event_new[log]:
                        for child in event.find("System"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        for child in event.find("EventData"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"

        if self.added_event_modified_ref is not None:
            output += "<u>Les logs suivants ont été ajoutés dans l'échantillon ET dans la référence mais n'ont pas été créés identiquement:</u></br>"
            for log in self.added_event_modified_ref.keys():
                if len(self.added_event_modified_ref[log]) > 0:
                    output += "### Dans le journal d'événements "+log+":</br>"

                    for i in range(0, len(self.added_event_modified_ref[log])):
                        event_1 = self.added_event_modified_ref[log][i]
                        event_2 = self.added_event_modified_sample[log][i]

                        output += "Log référence:</br>"
                        for child in event_1.find("System"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        for child in event_1.find("EventData"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        output += "</br>"
                        output += "Log echantillon:</br>"
                        for child in event_2.find("System"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        for child in event_2.find("EventData"):
                            output += str(child.tag)+": "+str(child.text)+"</br>"
                        output += "-----------------</br>"
                    output += "</br>"


        try:
            fichier = open("../results/readable_result/"+self.xml_ref_path.split('/')[-1].split('.')[-2]+".html", "wb")
            fichier.write(output.encode('ascii', 'xmlcharrefreplace'))
            fichier.close()
            print("Resultat lisible pour la VM "+self.xml_ref_path.split('/')[-1].split('.')[-2]+" disponible à ce lien : /results/readable_result/"+self.xml_ref_path.split('/')[-1].split('.')[-2]+".html")
        except IOError as io:
            print("Problème avec le fichier de resultat, celui ne sera pas créé")
        
                    






        
