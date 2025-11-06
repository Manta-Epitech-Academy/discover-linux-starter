# FAQ

### FAQ Déroulé:

> Impossible de scroller vers le haut, donc pour les affichages qui dépassent la taille de l'écran on ne pouvait pas voir le début.

L'atelier utilise un TTY, il n'y a pas de scroll dans un TTY par défaut. Il faut guider le participant sur l'utilisation de la commande `less` et bien lire ce qui est affiché à l'écran avant de faire apparaitre du texte à nouveau. Ce n'est donc pas un bug, c'est une fonctionnalité.

> Le participant est perdu, il ne sait pas ce qu'il faut faire.

L'atelier est conçu comme une sorte de RPG en "monde ouvert". Les quêtes peuvent êtres faite dans pratiquement n'importe quel ordre, *MAIS* il y a un ordre logique qui permet au participant de récolter des indices (accessibles via la commande `player`). Il ne faut pas hésiter à mettre une quête de côté car on a pas encore les ressources nécessaire (la connaissance que la commande X existe) pour terminer la quête et aller chercher une autre quête.

### Comment ça fonctionne ?

Le projet utilise [v86](https://copy.sh/v86/), un émulateur x86 dans le navigateur.
Et v86lab: un wrapper pour v86 qui permet de facilement créer des VM Linux dans le navigateur avec le support réseau entre les VM.

Une version déjà déployée est accessible sur [https://lab.epitech.academy/discover-linux-starter/](https://lab.epitech.academy/discover-linux-starter/) et [https://lab.epitech.academy/discover-linux-1/](https://lab.epitech.academy/discover-linux-1/)

### Comment lancer l'atelier ?

1. Cloner le dépôt GitHub
2. Lancer `./build_all.sh`
3. Servir le dossier `v86lab/dist` avec un serveur HTTP 
    - par exemple `cd v86lab/dist ;python3 -m http.server` (pas recommendé en production)
    - avec Apache/Nginx
4. Ouvrir un navigateur web moderne (Chrome, Firefox, Edge) et aller à l'adresse du serveur HTTP (par exemple `http://localhost:8000`)
    - Pour se rendre dans l'environnement de l'atelier: `cd /tmp/game_map` (les fichiers sont dans /tmp pour tout charger en RAM du navigateur et éviter de nombreuses requêtes sur le serveur HTTP lors des accès disques)

### Le build prend du temps, est-ce normal ?

Oui. L'étape la plus longue est la création d'une image de la RAM de la machine virtuelle (pour éviter aux participants d'avoir à attendre durant tout le processus de démarrage de Linux).

### Quel backend est utilisé ?

Aucun. Tout est exécuté dans le navigateur. Il suffit de servir le dossier `v86lab/dist` avec un serveur HTTP.

### La page web prend trop de temps à charger, que faire ?

- Le chargement initial est long car il faut télécharger une image disque de centaines de Mo.
- Utiliser un serveur HTTP proche des participants (même réseau local) pour réduire la latence.
- Patienter


### Peut-on dérouller l'atelier directement sur un PC ?

Oui. Il suffit d'utiliser l'image Docker fournie par le Dockerfile: v86lab/Dockerfile.alpine_image

### Peut-on dérouller l'atelier directement sur un PC sans Docker ?

Oui. Il suffit d'installer tous les fichiers nécessaires présent dans v86lab/home101/shell_rpg_engine

### Peut-on se soft-lock durant l'atelier ?

Oui. L'atelier utilise les véritables commandes Linux. Il est possible de se soft-lock en supprimant des fichiers nécessaires au déroulement de l'atelier.

- Utiliser v86lab ou Docker permet de repartir d'une image propre en cas de problème.
- Utiliser v86lab permet de facilement sauvegarder/charger l'état d'une partie. Il faut encourager les participants à le faire régulièrement.

Plus-value pédagogique: savoir se sortir d'une situation délicate est une compétence intéressante à avoir. Faire des sauvegardes régulières est une bonne pratique.

### Comment rajouter une quête ?

Il faut éditer `v86lab/home101/shell_rpg_engine/quests/npc_def.py`.
Dans ce fichier vous pouvez trouver la representation du monde du jeu sous forme de dictionnaire Python.
Vous pouvez ajouter un npc à une zone en rajoutant une entrée dans la liste associée à la clé de cette zone.
Vous pouvez ajouter une liste de quêtes à un npc en rajoutant une entrée dans la liste associée à la clé "quests" de ce npc et spécifier les conditions de réussite (dans une classe Python), il est également possible d'ajouter des hooks par exemple pour lancer du code après la validation d'une quête.
Vous pouvez relier les quêtes entre elles en utilisant un système de dépendence grâce aux clés: "must_done" et "must_doing"

### Je veux customiser l'environnement Linux, comment faire ?

Il faut éditer le Dockerfile v86lab/Dockerfile.alpine_image et rajouter tout ce que vous voulez dans l'image Docker.
Lors du build, l'image Docker est convertie en image disque pour v86.

### Comment le participant progresse dans le RPG ?

Le participant progresse en utilisant les commandes Linux pour interagir avec le monde du jeu.
Comme dans un RPG classique, le participant peut se déplacer et parler aux NPCs. Il faut parler aux NPCs pour obtenir ET rendre des quêtes (il n'y a pas de système d'event en dehors des actions du joueur: pour faire simple tout se fait via la commande `talk`).

Le participant peut faire les quêtes dans l'ordre qu'il souhaite (si les prérequis de quêtes sont rempli). Mais il y a un ordre "optimal" pour faire les quêtes dans le but d'obtenir des commandes Linux qui permettront de faire les quêtes suivantes.

Lorsqu'une quête est rendue, le joueur peut obtenir des récompenses: certaines de ces récompenses sont des commandes Linux qui pourront être utilisées pour progresser dans le jeu. (La commande `player` permet de voir l'état du joueur: les quêtes en cours, les quêtes terminées, les commandes obtenues, etc.)

### Un participant peut-il tricher ou utiliser des moyens pour contourner les quêtes ?

Oui. Rien ne l'empêche d'utiliser des commandes Linux pour lire les fichiers de NPCs ou modifier son état.
Les commandes Linux sont utilisées telles quelles, il n'y a pas de surcouche qui empêche de faire des actions non prévues par le jeu.

### Je dois debugger une partie, comment faire ?

Vous pouvez avoir un shell root en utilisant la commande `su` (aucun mot de passe, il suffit d'appyer sur Entrée lorsque le mot de passe est demandé).

### J'ai trouvé un bug, comment le signaler ?

Vous pouvez ouvrir une issue sur le dépôt GitHub du projet
