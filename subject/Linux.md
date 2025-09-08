
# Contexte

Partez à la découverte de Linux, un système d’exploitation libre et open source.
Vous apprendrez à utiliser la ligne de commande pour naviguer dans le système de fichiers, manipuler des fichiers et des répertoires et bien plus encore.

L'instroduction de cet atelier vous demandera de réaliser des quêtes à la manière d'un jeu de rôle (RPG) en ligne de commande. Vous incarnerez un personnage qui devra accomplir des missions en utilisant des commandes Linux.

## Pré-requis

Cet atelier nécessite l'accès à un terminal Linux.

- Si vous disposez d'une machine Linux, vous pouvez utiliser le terminal intégré.
- Si vous utilisez Windows, vous pouvez installer WSL (Windows Subsystem for Linux) ou utiliser une machine virtuelle avec une distribution Linux.
- Vous pouvez également vous rendre sur v86lab pour utiliser un terminal Linux en ligne (Méthode la plus simple et recommendée).

\newpage

# Fonctionnement de l'atelier d'introduction

Les dossiers représentent différentes zones du monde virtuel que vous allez explorer.
Afin de savoir ce qu'il y a dans une zone, vous pouvez utiliser la commande `ls` (*L*ist *D*irectory) pour lister les fichiers et dossiers qu'elle contient.
Les fichiers que vous allez rencontrer peuvent porter les extensions suivantes :
- `.npc` : personnages non-joueurs (PNJ) avec lesquels vous pouvez interagir à travers la commande `talk` suivie du fichier représentant le PNJ.
  - Exemple : `talk toto.npc`
  Les PNJ vous donneront des informations ou des quêtes à accomplir. N'hésitez pas à leur parler plusieurs fois, certains PNJ peuvent vous donner plusiers quêtes.
- '.obj' : objets avec lesquels vous pouvez interagir à travers différentes commandes afin de réaliser vos quêtes. Lisez attentivement les descriptions des quêtes pour savoir comment interagir avec les différents objets.
Vous pouvez changer de zone en utilisant la commande `cd` (*C*hange *D*irectory) suivie du nom du dossier représentant la zone.
  - Exemple : `cd village`
Pour revenir à la zone précédente, vous pouvez utiliser la commande `cd ..`
Afin d'obtenir des informations sur votre personnage, vous pouvez utiliser la commande `player`.

```bash
Vous vous réveillez au milieu d'une route, sans aucun souvenir de comment vous êtes arrivé là.
En fait, vous avez perdu presque toute votre mémoire.
La seule chose dont vous vous souvenez est :
- pour marcher : cd <zone>
- pour revenir à l'emplacement précédent : cd ..
- pour regarder autour de vous : ls
- pour parler : talk <pnj>
- pour avoir des informations sur vous : player
```

\newpage

# Tutoriel sur l'utilisation de v86lab

v86lab est un émulateur de machine virtuelle qui vous permet d'exécuter un système d'exploitation Linux directement dans votre navigateur web. Voici un tutoriel pour vous aider à démarrer avec v86lab :

### **Accéder à v86lab** :

Ouvrez votre navigateur web et rendez-vous sur le site de v86lab, l'environnement se chargera automatiquement (cela peut prendre quelques instants).

### **Sauvegarder votre progression** :

À tout moment, vous pouvez sauvegarder votre progression en cliquant sur le bouton "Save" situé en haut à gauche de l'écran. Cela téléchargera un fichier de sauvegarde sur votre ordinateur.
![v86lab_save1](v86save1.png "save"){width=700px}
![v86lab_save2](v86save2.png "save2"){width=700px}

### **Charger une sauvegarde** :

Pour charger une sauvegarde, cliquez sur le bouton "Load" et sélectionnez le fichier de sauvegarde que vous avez précédemment téléchargé. Cela restaurera l'état de la machine virtuelle à partir de ce fichier.
![v86lab_load](v86load.png "load"){width=700px}

### **Réinitialiser l'environnement virtuel** :

Si vous souhaitez réinitialiser la machine virtuelle à son état initial, vous pouvez tout simplement rafraîchir la page de votre navigateur. Attention cela veut dire également que vous pouvez perdre votre progression si vous quittez ou rechargez la page sans avoir sauvegardé.
