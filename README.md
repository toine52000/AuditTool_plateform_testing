*Projet de création d'une plate-forme de tests pour l'outil "AuditTool". Cette plate-forme permet le test d'executions de logiciels sur l'ensemble des éditions Windows, la récupération de résultats et l'analyse automatique de ceux-ci en observant les différents changements intervenants au niveau du système de fichier, des logs sytèmes et des registres.*


# I - Fonctionnement général de la plateforme
***********

Le but de la plate-forme est de tester des exécutables Windows dans le but de voir les différents changements (prévus ou imprévus) que le logiciel créera durant son exécution et plus particulièrement une application développé par le Bureau Audit et Inspection de l'ANSSI. Elle prend donc en entrée un exécutable et crée en sortie des rapports d’exécution démontrant les changements intervenus au niveau du système de fichiers, des registres et des logs de l'OS. Ces rapports sont lisibles humainement et sans trop de difficulté. Cette plate-forme teste les exécutables sur l'ensemble des versions, des éditions et des architectures des OS Microsoft Windows (depuis Windows XP et Windows Server 2003).

Afin de pouvoir tester les applications sur l'ensemble des versions de Windows, la plateforme utilise un serveur de virtualisation VMware ESXi ayant autant de machines virtuelles (VMs) qu'il y a d'OS de Windows (soit 225 versions).

Cette plateforme se divise en plusieurs parties distinctes:
* La partie "Installation" ou "Preliminary": Le but de cette partie est d'installer le serveur ESXi ainsi que l'ensemble des VMs qui serviront d'environnement d'exécution aux exécutables et les références de bases afin de pouvoir différencier l'avant/après exécution.
* La partie "Tests" ou "Platform": Elle a pour but de récupérer l'exécutable à contrôler, l'envoyer sur l'ensemble des VMs, lancer son exécution, attendre la fin de son exécution et récupérer les résultats de l'exécutable ainsi que les informations pouvant être utiles à la création des rapports d'analyse.
* La partie "Analyses" ou "Analysis": Le but de cette partie est d'analyser les différentes informations pouvant être utiles à la créations des rapports, concernant le système de fichiers, les registres systèmes et les journaux d'événements.
* La partie "Web": Elle permet la liaison entre les différentes parties de la plate-forme et permet l’interaction avec l'utilisateur.

## 1 - La partie "Installation"
TODO
Système de boucle/ Fichier BDD/ emplacement différents fichiers/ packer/ install guest tools/ 1er snap 

## 2 - La partie "Tests"
TODO
Système de Vague/ Différentes étapes/ Emplacement résultats/ Perf

## 3 - La partie "Analyses"
TODO
vmware-mount/ diff/ XML de sortie/ Cuckoo/ Resultats d'AT


ToDo

# II - Installation du serveur ESXi (serveur de virtualisation)
***********

La gestion des machines virtuelles se fait à l'aide d'un serveur de virtualisation VMware ESXi. Le téléchargement de l'image disque (ISO) du serveur ESXi est gratuit après inscription au site internet de VMware (https://my.vmware.com/web/vmware/registration). Il existe trois licences différentes à ce jour:
* Version d'essai: Elle peut être utilisée mais devra être réinstallée tous les 2 mois (possibilitée de garder les VMs créées)
* Version gratuite: Ne peut pas être utilisée (administration du serveur et des VMs non disponible)
* Version payante: Meilleure option (illimitée et sans contrainte de fonctionnement)

Les indications ci-dessous sont baséés sur l'ESXi version 6.0 (hors VSphere - les versions supérieures ne devraient pas poser de problèmes). Tous les exemples cités plus bas font référence à l'archirtecture réelle de la plateforme au sein de l'ANSSI.

## Création de l'ISO d'installation 

1. Après inscription auprès du site vmware officiel, télécharger l'ISO contenant l'installateur de l'OS serveur ESXi (sur [vmware.com](http://vmware.com) ou directement [sur la page de téléchargement de VMware](https://my.vmware.com/web/vmware/searchresults#site=my_download&client=my_download&getfields=*&output=xml_no_dtd&filter=0&proxyreload=1&proxystylesheet=my_download_en&num=10&entqr=3&start=0&q=ESXi&dscaf=__&requiredfields=dsca_lang:en&ie=UTF-8&ulang=en&access=p&entqrm=0&oe=UTF-8&ud=1&sort=date:D:S:d1))

2. Installer l'ISO sur un DVD bootable (avec des outils comme le graveur de DVD Windows par exemple)

## Installation de l'OS

1. Insérer le DVD d'installation dans le lecteur DVD de votre serveur.
(À prévoir, selon la configuration de votre serveur, mettre le boot sur DVD en priorité 1 dans le "Device Boot Order")

2. Le système d'installation va vous demander d'accépter les conditions d'utilisation, de choisir sur quel disque logique installer l'OS (prévoir beaucoup de place pour vos futures machines virtuelles), de choisir la langue du serveur et enfin un mot de passe pour l'utilisateur "root".

3. Une fois l'ensemble des fichiers chargés et copiés, votre serveur dispose d'un OS ESXi.


## Configuration 

### Configuration directement sur le serveur ESXi, avant mise en réseau:


1. Changement du mot de passe

Vous pouvez à présent changer le mot de passe de l'administrateur "root" pour plus de sécurité. Pour cela, sur la page d'accueil du serveur nouvellement installé, faire "F2" puis entrez les identifiants "root". Une fois dans le menu "System Customization", séléctionnez "Configure Password" et entrez l'ancien mot de passe puis deux fois le nouveau mot de passe voulu.

2. IP statique

Afin que le serveur soit accessible facilement, il doit être pouvu d'une adresse IPv4 statique. Pour cela, sur la page d'accueil du serveur, faire "F2" puis entrez puis entrez les identifiants "root". Une fois dans le menu "System Customization", séléctionnez "Configure Management Network" puis entrez les informations voulues pour les items suivants:
* Network Adapters (ex: vmnic0 Port 1)
* IPv4-> "Set Static IPv4 address and network configuration"
	* IPv4 Address (ex: 10.200.16.239)
	* Subnet Mask (ex: 255.255.252.0)
	* Default Gateway (ex: 10.200.16.1)
* IPv6 -> "Disable IPv6"

Vous pouvez maintenant quitter le menu de gestion réseau en appuyant sur "ECHAP" puis en acceptant de redémarrer le serveur ("Y"). Vous n'avez à présent plus besoin de vous connecter directement sur le serveur ESXi, les outils d'administration à distance VMware sont maintenant utilisable.

### Configuration en utilisant les outils d'adminitration de VMware, après mise en réseau du serveur:
Il est possible d'utiliser les outils VMware pour administrer totalement le serveur et ses VMs à distance. Cela permet un confort d'utilisation souvent très utile et préférable. Pour cela, il vous suffit d'installer le logiciel "VMware vSphere Client" sur un OS Windows connecté à un réseau capable d'atteindre le serveur. Pour le télécharger, rendez-vous via un navigateur internet à l'adresse IP de votre serveur ESXi précisées précédemment (ex: http://10.200.16.239/), comprenez les risques liés aux certificats puis cliquez sur "Download vSphere Client for Windows". Après installation, il vous suffit de le lancer puis de préciser l'adresse IP du serveur avec des identifiants valides.

3. Création d'un nouvel utilisateur

Il est intéressant, pour des raisons de sécurité ou de sureté de fonctionnement, de créer un utilisateur aux droits restreints afin que la plateforme puisse fonctionner sans avoir les pleins droits sur le serveur.

Dans "VMware vSphere Client", cliquez sur le serveur de virtualisation portant l'adresse IP précédemment donnée, puis, dans les onglets du cadre central, choisissez "Utilisateurs". Faites "clique droit" -> "ajouter...".

Entrez les informations suivantes:
* Connexion: attester
* Nom: Utilisateur de la palteforme de tests des outils Windows
* Mot de passe: CeQueVousSouhaitez**** (> 7 lettres, que minuscule/majuscule/chiffre) (ex: aAbBcC123)
* Confirmation: CeQueVousSouhaitez****

Vous devez maintenant lui donner les droits minimum à l'utilisation de la plate-forme. Pour cela, vous devrez d'abord créer un nouveau rôle limité puis l'appliquer à l'utilisateur que vous venez de créer. Pour créer un nouveau rôle, cliquez sur "Affichage" dans le barre d'outils, "Administration" puis "Rôles" dans le menu déroulant et enfin sur "Ajouter rôle" dans la nouvelle fenêtre qui s'affiche.

ToDo -> quel droit donner?

Pour assigner le nouveau rôle au nouvel utilisateur, cliquez sur l'onglet "Autorisations" puis faites clique droit et "Ajouter autorisation...". Dans le cadre "utilisateurs et groupes" appuyer sur "Ajouter..." et séléctionnez l'utilisateur précédemment créé.

4. SSH

Afin de récupérer les résultats des tests et de mieux gérer le serveur, une connexion SSH doit être possible auprès du serveur.

Pour cela, vous devez autoriser les flux à travers le port 22 sur le pare-feu du serveur en vous rendant dans l'onglet "Configuration" puis en cliquant sur "Profil de sécurité" du cadre "Logiciel". Cliquez ensuite sur "Prioriétés..." correspondant à "Pare-feu" et cochez "Client SSH" et "Serveur SSH".

De plus, il vous faut activer les services SSH en cliquant sur "Prioriétés..." correspondant à "Services". Séléctionnez "SSH" puis "Options...". Vous pouvez maintenant "Démarrer" le service en cliquant sur le bouton correspondant. Prenez soin de séléctionner "Démarrer et arrêter avec hôte" avant de confirmer.

Il faut maintenant redémarrer le serveur pour que les changements prennent effets.

Vous pouvez maintenant vous connecter au serveur ESXi via la commande  `ssh username@ip` avec username=l'utilisateur précédemment créé et ip=adresse de votre serveur. Une fois la première connexion faite, vous pouvez vous déconnecter du serveur via la commande `exit`.

5. Vérifier le nom du datastore

L'ensemble des VMs seront stockées dans le même datastore de l'ESXi pour de meilleures performances. Pour l'utilisation de la plateforme, vous devez préciser le nom de ce datastore. Une des choses à faire est donc de vérifier que celui-ci s'appelle bien "datastore1" comme c'est le cas par défaut. Pour cela, via un navigateur internet (une erreur de sécurité peut apparaître), vous vous connectez à l'adresse IP de votre serveur (ex: http://10.200.16.239/), puis cliquez sur "Browse datastores in this host's inventory" puis entrez des identifiants valides. Cliquez sur votre datacenter (par défaut "ha-datacenter") puis apparaît le nom du datastore par défaut.

Si jamais aucun datastore n'existe, simuler la création d'une VM puis supprimer cette VM et recommencer la démarche ci-dessus, cela aura pour conséquence de créer un datastore.

6. Création des Networks

La plate-forme doit disposer de deux cartes réseaux reliées au même réseau connecté à internet (ex: le réseau 10.200.16.1(255.255.252.0)) et de plusieurs réseaux virtuels différents ayant chacun leurs fonctions:
* Management Network: Pour administration de l'ESXi, doit avoir un seul IP qui est celui spécifié à l'installation de l'OS ESXi (ex: 10.200.16.239).
* VM Network: Réseau regroupant l'ensemble des VMs utiles à la plateforme, il n'est relié à aucune carte réseau physique.
* Web Network: Réseau pour accéder au serveur, qui fera lui même la passerelle avec les VMs (relié à une carte physique).

Pour configurer  les réseaux, cliquez sur l'onglet "Configuration" puis "Mise en réseau".
Pour ajouter un nouveau réseau, cliquez sur "Ajouter une mise en réseau"-> "Machine Virtuelle"-> choisissez la carte réseau de votre serveur adéquate-> renommez le réseau. Vous devez obtenir le schéma suivant:

![voir image master/doc/reseaux-exemple.png](reseaux-exemple.png)



# III - Installation du serveur Web et de gestion de la plate-forme
***********
Pour de meilleures performances, le serveur web gérant la plate-forme sera présent au sein même du serveur de virtualisation qu'il utilise. Il pourra ainsi profiter des capacités du serveur. Ce serveur gérera les différents scripts de la plate-forme, affichera les résultats obtenus, installera les VMs de test et récupérera l'éxecutable à tester.

ATTENTION - Si vous donnez un autre nom à la VM du serveur que "server", la plateforme considérera la VM comme une VM de test ce qui impliquera la perte du serveur.

ATTENTION - La VM doit être sous un système d'exploitation Linux. Elle a été testée sous linux Debian 7.7 mais devrait fonctionner sous n'importe quel autre os Linux.

Pour créer la VM, faites "clique droit" sur le serveur puis "Nouvelle Machine Virtuelle" puis séléctionnez:
* Configuration: Personnalisée
* Nom: server
* Lieu de stockage: datastore1
* Version : 11
* Système d'Exploitation: Linux puis choisissez la version voulue
* Nombre de Socket: 4 / Nombre de Noyaux: 4
* Mémoire : 32Go
* Nombre de cartes NIC:2
	* NIC 1: Web Network / Adapteur: E1000 / Connecter à mise sous tension
	* NIC 2: VM Network / Adapteur: E1000 / Connecter à mise sous tension
* Disque: Créer un disque Virtuel
* Taille: 200Go (pour pouvoir stocker les ISOs)


## 1 - Installation de l'OS & généralitées

Nous ne détaillerons pas la façon d'installer un OS (cela dépend de l'OS voulu). Pour plus d'information se référer aux différents exemples disponible sur internet ou sur [la documentation vSphere](https://pubs.vmware.com/vsphere-51/index.jsp#com.vmware.vsphere.solutions.doc/GUID-91F2410C-DF89-4F98-8112-CF0D00400E23.html).



### Configuration réseau

La première chose à faire est de vérifier la correspondance entre les cartes réseaux virtuelles et les interfaces (eth0, eth1...) de notre serveur. Pour cela, faites "clique droit" sur le serveur dans la liste des VMs puis "Modifier les paramètres..." et relevé les adresses MAC de vos deux adapteurs réseau:

`Adapteur1 - Web Network - 00:0c:29:2f:8f:74
Adapteur2 - VM Network - 00:0c:29:2f:8f:7e`

Puis, dans votre VM "server", en mode root, faites `ifconfig`:

`eth0 ... HWaddr 00:0c:29:2f:8f:74...
eth1 ... HWaddr 00:0c:29:2f:8f:7e...`

Dans notre cas, on voit donc que l'interface eth0 sera l'interface connectée au réseau "Web Network" et eth1 l'interface connectée au réseau "VM Network". On va donc les configurer pour avoir accès à ces réseaux:


Désactiver le service network-manager:

`/etc/init.d/network-manager stop
chmod -x /etc/init.d/network-manager`


Modifier les interfaces:

`vi /etc/network/interfaces`

Entrez les informations suivantes (10.200.16.238 = IP statique réseau internet à modifier selon le réseau internet de votre serveur / = IP statique réseau des VMs):

`auto eth0
iface eth0 inet static
	address 10.200.16.238
	netmask 255.255.252.0
	gateway 10.200.16.1
auto eth1
iface eth1 inet static
	address 192.168.0.2
	netmask 255.255.255.0
	gateway 192.168.0.1`



Configuration DNS:

`vi /etc/resolv.conf`

`nameserver 8.8.8.8
nameserver 8.8.4.4`


Redémarrer le service networking:

`/etc/init.d/networking restart`


Vous devez maintenant être capable de "pinger" le serveur ESXi (10.200.16.239) et votre passerelle (10.200.16.1).


### Configuration sources.list

Modifier le fichier sources.list pour pouvoir utiliser le gestionnaire de paquet APT:

`vi /etc/apt/souces.list`

Supprimer tous et remplacer par:

`deb http://httpredir.debian.org/debian jessie main contrib non-free
deb-src http://httpredir.debian.org/debian jessie main contrib non-free
deb http://httpredir.debian.org/debian jessie-updates main contrib non-free
deb-src http://httpredir.debian.org/debian jessie-updates main contrib non-free
deb http://security.debian.org/ jessie/updates main contrib non-free
deb-src http://security.debian.org/ jessie/updates main contrib non-free`

Mettre le système à jour:

`apt-get update
apt-get dist-upgrade`

### Configuration des droits via sudo

On donne les droits root à l'utilisateur créé à l'installation de l'OS (dans notre cas server-admin):

`sudo apt-get install sudo`

`vi /etc/sudoers
server-admin	ALL=(ALL:ALL) ALL`

`adduser user sudo
shutdown -r now`

A partir de maintenant, toutes les configurations se feront à l'aide de l'utilisateur créé à l'installation via sudo.

### Installation des VMware Guest Tools

Pour de meilleure performances et une meilleures gestion des drivers, installer les VMware Guest Tools:

`sudo apt-get install open-vm-tools
shutdown -r now`

### Téléchargement de la plateforme 

Plusieurs possibilités sont envisageable pour télécharger la plateforme:

1. Directement à partir du dépôt gitlab via l'outil git (git@gitlab.cossi.internet:amartin/AuditTool-Testing-Plateform.git)
2. Directement à partir du dépôt gitlab en téléchargeant l'archive (https://gitlab.cossi.internet/amartin/AuditTool-Testing-Plateform/repository/archive.zip)
3. Soit en poussant l'archive via SSH en utilisant une autre station de travail (`scp archive.zip server-admin@10.200.16.238:~`)

Il vous faut aussi récupérer les fichiers ISOs contenant les installateurs des différentes versions de Windows:

TODO

## 2 - Prérequis partie "Installation"


### Installation de python3.5 et python2.7

Télécharger la version de python3.5 correspondant à votre système sur le lien suivant https://www.python.org/downloads/

`tar -xvzf Python-3.5.2.tgz
cd Python-3.5.2
sudo apt-get install build-essential
./configure
make
make test
sudo make install`


`sudo apt-get install python2.7`


### Installation de la bibliothèque pyVmomi

`wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py 
sudo ./get-pip.py
sudo pip install pyvmomi -t /usr/lib/python3/dist-packages`


### Ouverture des ports VNC

VNC est utilisé par l'outil packer.io utilisé pour créer les VMs automatiquement. Il lui permet d'envoyer des commandes à la VM qui vient d'être créée.

Pour cela, sur le serveur ESXi (physiquement ou via `ssh root@10.200.16.239`), lancer la commande suivante:

`esxcli system settings advanced set -o /Net/GuestIPHack -i 1`

puis le script suivant pour ouvrir les ports nécessaires à Packer (port VNC):

`mkdir /store/firewall`

 // Copie service.xml -> règles firewall 

`cp /etc/vmware/firewall/service.xml /store/firewall`


 // Ajout de la règle VNC

`sed -i "s/<\/ConfigRoot>//" /store/firewall/service.xml
echo "
  <service id='0041'>
    <id>vnc</id>
    <rule id='0000'>
      <direction>inbound</direction>
      <protocol>tcp</protocol>
      <porttype>dst</porttype>
      <port>
        <begin>5900</begin>
        <end>5950<end>
      </port>
    </rule>
    <enabled>true</enabled>
    <required>false</required>
  </service>
</ConfigRoot>" >> /store/firewall/service.xml`

 // Copie du fichier de configuration firewall à l'emplacement prévu puis on relance le service firewall

`cp /store/firewall/service.xml /etc/vmware/firewall/service.xml`

 // On créé une règle locale pour la persistence

`sed -i "s/exit 0//" local.sh
echo "
cp /store/firewall/service.xml /etc/vmware/firewall/service.xml
esxcli network firewall refresh
exit 0" >> /etc/rc.local.d/local.sh`

 // On redémarre le service firewall

`esxcli network firewall refresh`

## 3 - Prérequis partie "Tests"
Cette partie nécessite uniquement python3 et la bibliothèqque pyvmomi, se référer à la partie précédente ci-ceux ne sont pas encore installé.

## 4 - Prérequis partie "Analyse"

### Installation de sshpass

`sudo apt-get install sshpass`

Faire un `ssh root@10.200.16.239` avant tout depuis "server", pour que la clé SSH soit ajoutée et que le script puisse ensuite faire des SSH en mode silencieux.

### Installation de vmware-mount

ATTENTION: à partir de la version 5.5 du vddk (Virtual Disk Development Kit), vmware-mount n'existe plus!

Rendez-vous sur https://developercenter.vmware.com/web/sdk/51/vddk et télécharger (il faut un compte vmware):
`wget https://developercenter.vmware.com/web/sdk/51/vddk
tar -xvzf VMware-vix-disklib-*.tar.gz
cd vmware-vix-disklib-distrib
sudo ./vmware-install.pl`

Accepter les conditions d'utilisation, le répertoire d'installation "/usr/" est recommandé.

## 5 - Prérequis partie "Web"

Installation de serveur apache classique (si pas le cas par défaut):

`sudo apt-get install apache2`
`sudo apt-get install php5`

# IV - Récupération du code source

Afin de rendre la plate-forme opérationnelle, il vous faut maintenant récupérer le code source de la plate-forme:
* Soit par git (le code source est stocké sur le dépot gitlab)
* Soit directement à partir du fichier ".zip"

il faut déposer l'ensemble du répertoire racine du code source directement dans le répertoire "/var/www/" et ainsi remplacer le dossier "html" normalement présent par défaut.


De plus, il vous faut récupérer l'ensemble des fichier ISOs présent sur le disque dur externe prévus à cet effet et copier dans le répertoire "/var/www/preliminary/packer/iso/".

Donnez les pleins droits à la plate-forme:
`su
chmod -R u+s /var/www/*`












