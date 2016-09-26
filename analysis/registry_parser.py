#!/usr/local/bin/python3.5

import sys
from Registry import *

class RegistryComparator:

    def __init__(self, registry_data_before, registry_data_after):

        #Tableau contenant des autres tableaux de clés supprimés/ ajoutés tel que:
        #[0]=path/[1]=nom de clé/[2]=valeur clé/[3]=type
        self.created_keys = []
        self.deleted_keys = []

        #Tableau contenant des autres tableaux de clés modifiés tel que:
        #[0]=path/[1]=nom de clé/[2]=valeur clé registre1/[3]=valeur clé registre2/[4]=type
        self.modified_keys = []

        #Tableau de string contenant le nom de path créé/supprimé
        self.created_path = []
        self.deleted_path = []

        #tableau provenant de la classe Registryparser
        #de la forme dict(path, list[keys, values]
        self.reg_data_before = registry_data_before
        self.reg_data_after = registry_data_after
        
    #Fonction permettant de comparer les données recceuillies par la classe RegistreParser
    #à partir de deux registres différents (reg_data_before/ reg_data_after).
    def registry_comparator(self):

        data_dict1 = self.reg_data_before
        data_dict2 = self.reg_data_after

        #On parcourt l'ensemble des paths du 1er registre
        for path in data_dict1:

            #Si le path est aussi présent dans le 2nd registre
            if path in data_dict2:

                key_list1 = data_dict1[path]
                key_list2 = data_dict2[path]

                #On parcourt l'ensemble des clés du path du 1er registre
                for dict_i in key_list1:
                    key_present = False
                    equal_value = False

                    #On parcourt l'ensemble des clés du path du 2nd registre
                    for dict_j in key_list2:

                        #Les noms des clés sont similaires aux deux registres
                        if dict_i[0]==dict_j[0] :
                            key_presente = True

                            #On supprime cette clé des données du 2nd registre pour ne pas
                            #à avoir à les recomparer par la suite -> performance
                            self.reg_data_after[path].remove(dict_j)
                        
                            #Les valeurs des clés sont similaires aux deux registres
                            if dict_i[1]==dict_j[1]:
                                equal_value = True
                                
                    #Si il n'y a plus de clé dans le path du second registre, on supprime
                    #le tableau pour ne pas à avoir à recomparer les paths par la suite
                    if len(self.reg_data_after[path]) == 0:
                        del self.reg_data_after[path]

                    #Si la clé est absente dans le second registre, on l'ajoute au tableau des
                    #clés supprimés
                    if key_presente == False:
                        self.deleted_keys.append([path, dict_i[0], dict_i[1], dict_i[2]])

                    #Si les deux clés n'ont pas les même valeurs, on les ajoute au tableau
                    #des clés modifiés (même nom de clé, 2 valeurs différentes)
                    if equal_value == False:
                        self.modified_keys.append([path, dict_i[0], dict_i[1], dict_j[1], dict_i[2]])

                        
            #Si le path n'est pas trouvé dans le 2nd registre
            else:

                #On ajoute le path au tableau des paths supprimés
                self.deleted_path.append(path)
                
                #On ajoute ses clés filles aux tableau des clés supprimés
                for dict_i in data_dict1[path]:
                    self.deleted_keys.append([path, dict_i[0], dict_i[1], dict_i[2]])

                    

        #on recommence maintenant l'analyse à partir des données du 2nd registre allégé
        #dans le but de trouver les path et clés créées
        data_dict1 = self.reg_data_before
        data_dict2 = self.reg_data_after

        #On parcourt les paths du 2nd registre
        for path in data_dict2:
                        
            #Si le path est aussi dans les données du 1er registre, alors c'est forcément une
            #nouvelle clé crée (le cas des clés modifiées a déjà été traités)
            if path in data_dict1:
                
                key_list1 = data_dict1[path]
                key_list2 = data_dict2[path]

                #on parcourt les clés du path du 2nd registre
                for dict_i in key_list2:
                    self.created_keys.append([path, dict_i[0], dict_i[1], dict_i[2]])

            #Si le path est absent dans les données du 1er registre
            else:
                #ajout du path créé dans le tableau des paths créé
                self.created_path.append(path)
                
                #Ajout des clés filles du path créé
                for dict_i in data_dict2[path]:
                    self.created_keys.append([path, dict_i[0], dict_i[1], dict_i[2]])
      

                 
    def print_changes(self):

        print("### PATH ###")
        print("\nI - Added path:")
        for i in self.created_path:
            print("- "+ i )
        print("\nII - Deleted path:")
        for i in self.deleted_path:
            print("- "+ i )

        print("\n### KEY ###")
        print("\nI - Added key:")
        for i in self.created_keys:
            print("- path:"+ i[0] +" key:"+i[1]+" type:"+i[3] +" value: "+i[2] )
        print("\nII - Deleted key:")
        for i in self.deleted_keys:
            print("- path:"+ i[0] +" key:"+i[1]+" type:"+i[3] +" value: "+i[2] )
        print("\nIII - Modified key:")
        for i in self.modified_keys:
            print("- path:"+ i[0] +" key:"+i[1]+" type:"+i[4] +" value1: "+i[2]+" value2: "+i[3] )
            



class RegistryParser:

    #Dictionnaire contenant les couples path/listes des clefs
    path_dict = {}

    def __init__(self):
         self.path_dict = {}

         
    def registry_data_extractor(self, key, depth=0):

        #liste contenant les dicitonnaires clé/valeur d'un même path
        key_list = []
        key_value_list= []

        #Ajout des clés/valeurs à la liste
        for v in key.values():

            key_value_list = []
            key_value_list.append(v.name())
            key_value_list.append(str(v.value()))
            key_value_list.append(v.value_type_str())
            key_list.append(key_value_list)

        path =  self.formatPath(key.path())
        self.path_dict.setdefault(self.formatPath(key.path()), key_list)

        #Idem pour sous-clés
        for subkey in key.subkeys():
                self.registry_data_extractor(subkey, depth + 1)

                

    def getRegistryDictPath(self):
        return self.path_dict

    def formatPath(self, temp_string):
        string_formated = ""
        group = temp_string.split("\\")
      
        if len(group) > 2:
            for i in range(1,len(group)):
                if i == 1:
                    string_formated = group[i]
                else:
                    string_formated += "\\" + group[i]
            return string_formated
        else:
           return "\\"


    def formatKey(self, temp_string):
        string_formated = ""
        group = temp_string.split("\\")
      
        if len(group) > 2:
            for i in range(1,len(group)):
                    string_formated += "\\" + group[i]
            return string_formated
        else:
           return "\\"
