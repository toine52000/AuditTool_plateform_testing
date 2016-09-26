#!/usr/bin/python3

import os
import sys
import time


from snapshot.initial_snapshot import takeInitialSnapshot

def packer(vm_name, iso_path, answers_file_path, config_path) :

	#Recuperation du checksum MD5
	retour=os.popen("md5sum packer/" + iso_path + " | cut -d' ' -f1").readlines()

	if retour is not None:
		checksum = retour[0]
		checksum = checksum[:-1]
	else:
		sys.exit("Veuillez installer l'utilitaire checksum")

	#Execution de l'executable packer
	print("packer/packer build -var vm_name=\""+vm_name+"\" -var answers-file=\""+answers_file_path+"\" -var iso_checksum=\""+checksum+"\" -var iso_path=\""+iso_path+"\" "+config_path)
    
	os.system("packer/packer build -var vm_name=\""+vm_name+"\" -var answers-file=packer/\""+answers_file_path+"\" -var iso_checksum=\""+checksum+"\" -var iso_path=packer/\""+iso_path+"\" "+"packer/"+config_path)
    
	return vm_name



if __name__ == "__main__" :
    
	old_vm = ""
	nom_vm = ""
	with open("packer/bdd.csv",'r') as f:	
		for line in f:

			#ignorer les lignes vides
			if line != "\n":

				#ignorer les lignes commentaires
				if line[0] != '#':

					info=line.split(";")

					#verification de bonne formation de la ligne recuperee
					if len(info) != 4:
						print("Erreur dans la base de donnee sur la ligne:", line, "\n")

					else:
						if nom_vm!="":
							old_vm=nom_vm			

						nom_vm=info[0]
						iso_path=info[1]
						answers_file_path=info[2]
						config_path=info[3]
                
						print("Traitement du systeme: "+nom_vm)
						packer(nom_vm, iso_path, answers_file_path, config_path)
	
						if (old_vm!= ""):
							print("prise du snapshot de la vm precedement cree: "+old_vm)
							takeInitialSnapshot(old_vm)

		print("Attente avant prise du dernier snapshot")
		time.sleep(600)
		takeInitialSnapshot(nom_vm)
				
			
	f.close()





