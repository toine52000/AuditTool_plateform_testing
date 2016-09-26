<?php
	$uploaddir = '/var/www/html/';
	$uploadfile = $uploaddir . basename($_FILES['new_exec']['name']);

	if ($_FILES['new_exec']['type'] == 'application/x-ms-dos-executable'){

	   if ($_FILES['new_exec']['name'] == 'audit_tool.exe' || $_FILES['new_exec']['name'] == 'audit_tool_x64.exe'){

	      if (move_uploaded_file($_FILES['new_exec']['tmp_name'], $uploadfile)) {
	      
		echo "Le fichier est valide et a été téléchargé avec succès. Vous pouvez retourner sur la page précédente";
	      } else {
    	        echo "Erreur lors de l'envoie, merci de réessayer";
	      }


	   } else {
	      echo "Vous devez obligatoirement nommé le fichier à envoyer audit_tool.exe ou audit_tool_x64.exe et non pas :".$_FILES['new_exec']['name'];
	   }
	} else {
	  echo "Vous devez obligatoirement envoyer un fichier de type exécutable Windows et non un fichier de type :".$_FILES['new_exec']['type'];
	}

?>