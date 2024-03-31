# TDIA1-linux-distro
Presentation de Notre TDIA1FS "TDIA1 FILE SYSTEM" :
Notre système de fichiers est basé sur le système de fichiers HADOOP et GFS "GOOGLE FILE SYSTEM". La visée de ce système distribué est de stocker des fichiers de façon sécurisée et d'une durée réduite .

La structure de TDIA1FS :
La structre de TDIA1FS est composé de trois serveurs : un serveur master qu'on appelait METRE et des serveur donnée avec une option de gérer la réplications de leurs blocs.
Et finalement ,  un serveur client qui va nous permet la connexion entre les serveurs données. Chaque serveur donnée est constitué de plusieurs blocs.

L'arborescence de TDIA1FS:
Ce système de fichiers est constitué de cinq répertoires "bin" && "data" && "config" && "log" && "config" && "etc".
chaque répertoire esr constitué des fichers , à titre d'exemple le "etc" qui contient tout qui est une relation avec les mots de passe et "config" qui contient tout qui est une relation avec la configuration.

Guide D'installation :
1/ Installation de VIRTUAL MACHINE.
2/ Modifier les paramètres de VMWARE ou VIRTUAL BOX.
3/ Lancement de notre ISO dans le VMWARE.
4/ Suivre les étapes d'installation.
5/ Set UP de l'utilisateur.

Voici notre distribution personnalisée : 
https://drive.google.com/file/d/1aYXDMylTrpsaDHFqoA30CuN2byPNqnnB/view?usp=sharing

Guide D'utilisation:
1/ Lancement de SETUP: run du script SETUP.
2/ Lancement de config.
3/ Modification si vous voulez les configurations concerenant les tailles des blocs , les adresses IP des serveurs_DONNE.
2/ Ouvrage d'un terminal en tant que serveur_METRE .
3/ Ouvrage d'un terminal en tant que serveur_CLIENT .
4/ Ouvrage deux et plus en tant que serveur_DONNEE .
5/ Lancement de script client dans serveur_CLIENT.
6/ Lancement de script maitre dans serveur_METRE.
7/ Lancemenet de script donnée dans serveur_DONNE.
8/ Lancement de script avec déclaration de port et de chemin data.
9/ TEST de commande dans terminal client .
