import os
import json
import shutil
import pwd
import random
import hashlib
import base64

base = "/tmp/game_map"

livres = [
    "Germinal",
    "Madame Bovary",
    "Les Miserables",
    "LEtranger",
    "La Chartreuse de Parme",
    "Voyage au bout de la nuit",
    "Candide",
    "La Peste",
    "Notre-Dame de Paris",
    "Le Pere Goriot",
    "Jacques le Fataliste",
    "Bel-Ami",
    "Le Comte de Monte-Cristo",
    "La Princesse de Cleves",
    "Une vie",
    "La Condition humaine",
    "Therese Raquin",
    "Les Fleurs du mal",
    "Aurelien",
    "Les Chants de Maldoror",
    "La Fortune des Rougon",
    "Les Rois maudits",
    "Le Rouge et le Noir",
    "Sylvie",
    "Indiana",
    "La Symphonie pastorale",
    "La Guerre de TRoie naura pas lieu",
    "Phedre",
    "Cyrano de Bergerac",
    "Les Nourritures terrestres",
    "Manon Lescaut",
    "Discours de la methode",
    "Le Mariage de Figaro",
    "La Mare au diable",
    "Les Confessions",
    "LAssommoir",
    "La Nausee",
    "LIle mysterieuse",
    "La Chartreuse du Nord",
    "Le Soulier de satin",
    "Colomba",
    "Meditations poetiques",
    "Le Livre de ma mere",
    "La Disparition",
    "Enfance",
    "Le Hussard sur le toit",
    "Les Justes",
    "Le Diable au corps",
    "Le Deuxieme Sexe"
]

def create_lake_files(n=200):
    treasure_base64 = "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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
    random.seed(42)
    objects = [
        "epave", "planche", "masque", "chaussure", "perle",
        "barque", "corail", "filet", "baril",
        "couvercle", "seau", "statue", "pagaie", "ancre", "pierre",
        "couronne", "seau_rouille", "lampe", "harnais",
        "crane", "os", "cloche",
        "parchemin", "boussole", "lanterne", "coquille", "roseau",
        "carpe", "brochet", "grenouille", "seau_perce", "pirogue",
        "seau_bois", "tesson",
        "idole", "coing", "bois_mouille", "seau_bois",
        "parfum", "poterie",
        "seau_argile", "tapis", "voile", "cordage", "carquois",
        "bouee", "chaudron", "seau_plomb", "chaussure_boueuse",
        "epingle", "clou", "poignee", "parasol",
        "seau_metal", "tabouret", "pied_statue", "tronc", "branche", "plume",
        "os_poisson", "sceau", "tombe", "pierre_gravee"
    ]

    obj = []
    for i in range(1, n + 1):
        name = f"{random.choice(objects)}_{i}"
        obj.append({
            "name": name,
            "desc": f"Un(e) {name} sans aucune utilité",
            "content": f"Un(e) {name} sans aucune utilité\n"
        })
    obj = [*obj, 
           {
            "name": "tresor.tar",
            "desc": "Un trésor mysterieux en format .tar, contenant des formules magiques.",
            "content": base64.b64decode(treasure_base64).decode('utf-8', errors='ignore')
           }]
    return obj

class QuestValidation:
    def __init__(self, quest, player, npc):
        self.player = player
        self.quest = quest
        self.npc = npc

    def pre_quest(self):
        pass

    def validate_quest(self):
        pass

    def post_quest(self):
        pass

class Checks:
    @staticmethod
    def get_subdir_count(path):
        return len([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    
    @staticmethod
    def input_str(prompt):
        return input(prompt).strip()
    
    @staticmethod
    def file_under_location(file_name, location):
        for root, dirs, files in os.walk(f"{base}/{location}"):
            if file_name in files:
                return True
        return False
    
    @staticmethod
    def file_hash_match(file_path, expected_hash):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'rb') as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest() == expected_hash
        

    @staticmethod
    def file_content_match(file_path, expected_content):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as f:
            content = f.read().strip()
            return content == expected_content

        
    @staticmethod
    def has_duplicate_in_dir(original_file, target_dir):
        original_hash = hashlib.sha256(open(original_file, 'rb').read()).hexdigest()
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file == os.path.basename(original_file):
                    continue
                file_path = os.path.join(root, file)
                if hashlib.sha256(open(file_path, 'rb').read()).hexdigest() == original_hash:
                    return True
        return False
    
    @staticmethod
    def file_is_a_symlink_to(file_path, target_path):
        if not os.path.islink(file_path):
            return False
        return os.readlink(file_path) == target_path 
    
    def lines_in_file_sorted_alphabetically(file_path, expected_lines):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as f:
            lines = f.read().strip().split('\n')
            return lines == expected_lines

class Mkdir(QuestValidation): # Quest giver: Kevin, Location: village

    def validate_quest(self):
        super().validate_quest()
        if Checks.get_subdir_count(f"{base}/village") >= 3:
            return True, "Bravo ! Vous avez créé 3 maisons dans le village."
        else:
            return False, "Vous devez créer 3 maisons dans le village en utilisant la commande mkdir."

class HiddenCreate(QuestValidation):  # Quest giver: Quentintin, Location: Village
    def validate_quest(self):
        super().validate_quest()
        village_path = f"{base}/village"
        hidden_dirs = [
            d for d in os.listdir(village_path)
            if d.startswith(".") and os.path.isdir(os.path.join(village_path, d))
        ]
        if hidden_dirs:
            hidden_path = os.path.join(village_path, hidden_dirs[0])
            os.system(f"mv {base}/village/Quentintin.npc {hidden_path}/")
            return True, f"Merci d'avoir créé une planque ({hidden_dirs[0]}) !"
        else:
            return False, "Crée-moi une planque (un dossier caché, commençant par '.')."


class Treasure(QuestValidation):
    def validate_quest(self):
        super().validate_quest()
        if os.path.isfile(f"{base}/montagne/tunnel/route_de_montagne/lac/tresor.tar"):
            return True, "Tonnerre de tonnerres ! Merci d'avoir repêché ce sacré trésor, mais maintenant, bougre d'explorateur d'eau douce, il va falloir l'ouvrir, nom d'un bachibouzouk !"
        else:
            return False, "Mille sabords ! Halte-là, moussaillons ! Ramenez ce trésor au bercail, droit au lac, et plus vite que ça, espèces de marins d'eau douce !"

class TreasureOpen(QuestValidation): # Quest giver: Quentintin, Location: Village
    def validate_quest(self):
        super().validate_quest()
        planque_path = os.path.join(f"{base}/village", ".planque")
        if os.path.isdir(f"{base}/montagne/tunnel/route_de_montagne/lac/tresor"):
            return True, "Tonnerre de Brest ! Bravo, moussaillon, tu as ouvert le trésor ! Mille millions de sabords, te voilà désormais en possession des deux formules magiques... ça pourra te servir plus tard, ou que le diable m'emporte !"
        else:
            return False, "Mille milliards de mille sabords ! N'oublie pas ta quête, moussaillon : ouvre le trésor et empare-toi des deux formules magiques, ou tu finiras marin d'eau douce à vie !"

class ReadFile(QuestValidation): # Quest giver: Kevin, Location: forest

    def validate_quest(self):
        super().validate_quest()
        if Checks.input_str("Veuillez lire le panneau pour moi : ") == "cd ../village":
            return True, "Merci d'avoir lu le panneau !"
        else:
            return False, "Ce n'est pas ce qui est écrit sur le panneau ! Veuillez réessayer."


class WhoIsThere(QuestValidation): # Quest giver: Paul, Location: village

    def validate_quest(self):
        super().validate_quest()
        if Checks.input_str("Veuillez me donner votre nom : ") == pwd.getpwuid(os.getuid()).pw_name:
            with open(f"{base}/village/outils.obj", 'w') as f:
                f.write("c047eaea91e27374")
            return True, "Merci de m'avoir donné votre nom !"
        else:
            return False, "Ce n'est pas votre nom ! Veuillez réessayer."


class Move(QuestValidation): # Quest giver: Jacques, Location: mountain

    def validate_quest(self):
        super().validate_quest()
        if Checks.file_under_location("Jacques.npc", "village") and not Checks.file_under_location("Jacques.npc", "montagne"):
            return True, "Enfin chez moi !"
        else:
            return False, "Veuillez m'aider à retourner au village."


class Fedex1(QuestValidation): # Quest giver: Worker, Location: .passage_secret

    def validate_quest(self):
        super().validate_quest()
        if Checks.file_content_match(f"{base}/montagne/.passage_secret/outils.obj", "c047eaea91e27374") or Checks.file_content_match(f"{base}/montagne/tunnel/outils.obj", "c047eaea91e27374"):
            return True, "Merci d'avoir apporté les outils !"
        else:
            return False, "Vous devez apporter les outils du village au passage secret."
        
    def post_quest(self):
        if os.path.isdir(f"{base}/montagne/.passage_secret"):
            os.rename(f"{base}/montagne/.passage_secret", f"{base}/montagne/tunnel")
            os.chmod(f"{base}/montagne/tunnel/route_de_montagne", 0o755)
            os.system(f"cd {base}/montagne/; bash --norc")



class Copy(QuestValidation): # Quest giver: Merchant, Location: mountainroad

    def validate_quest(self):
        super().validate_quest()
        if Checks.has_duplicate_in_dir(f"{base}/montagne/tunnel/route_de_montagne/roue.obj", f"{base}/montagne/tunnel/route_de_montagne"):
            return True, "Bravo ! Vous avez copié la bonne roue."
        else:
            return False, "Vous devez copier le contenu de la bonne roue."


class SortBooks(QuestValidation): # Quest giver: Servant, Location: castle

    def validate_quest(self):
        super().validate_quest()
        library_path = f"{base}/montagne/tunnel/route_de_montagne/vallee/chateau/bibliotheque"
        for file in os.listdir(library_path):
            if file.endswith(".obj"):
                path = f"{library_path}/{file}"
                attendu = "\n".join(sorted(livres)) + "\n"
                with open(path, "r") as f:
                    contenu = f.read()
                if contenu == attendu:
                    return True, "Merci d'avoir trié les livres !"
        return False, "Vous devez trier les livres dans la bibliothèque."


class Shortcut(QuestValidation): # Quest giver: Guard, Location: dungeon

    def validate_quest(self):
        super().validate_quest()
        dungeon_path = f"{base}/montagne/tunnel/route_de_montagne/vallee/chateau/donjon"
        if Checks.file_is_a_symlink_to(f"{dungeon_path}/raccourci", f"{base}/village/"):
            return True, "Vous avez créé un raccourci vers le village !"
        else:
            return False, "Vous devez créer un raccourci vers le village."


class HiddenFile(QuestValidation): # Quest giver: Kevin, Location: forest

    def validate_quest(self):
        super().validate_quest()
        if Checks.input_str("Quel est le contenu de la carte du passage secret ?") == "cd ../montagne/.passage_secret":
            self.post_quest()
            return True, "Vous avez trouvé la carte du passage secret !"
        else:
            return False, "Vous devez trouver la carte du passage secret dans la forêt."

    def post_quest(self):
        os.chmod(f"{base}/montagne/.passage_secret", 0o755)
        os.chmod(f"{base}/montagne/.passage_secret/route_de_montagne", 0o600)


class AcceptShell(QuestValidation): # Quest giver: Fisherman, Location: sea
    def validate_quest(self):
        super().validate_quest()
        if Checks.input_str("Voulez-vous le joli coquillage ? (oui/non) ") == "oui":
            return True, "Merci d'avoir accepté le joli coquillage !"
        else:
            return False, "D'accord, demandez-moi à nouveau si vous le voulez."
        
    def post_quest(self):
        os.system('export PS1="\\u@\\h \\w> "; exec bash --norc')
        
class AlwaysValid(QuestValidation): # For any quest that is always valid: For example, to give something to the player or print some lore related messages and progress in the story.

    def validate_quest(self):
        return True, ""

class KingSummons(AlwaysValid):  # Quest giver: Roi, Location: chateau
    def post_quest(self):
        os.system(
            f"mv {base}/montagne/tunnel/route_de_montagne/vallee/chateau/salle_du_trone/Roi.npc {base}/foret/mer/"
        )
        mer_path = f"{base}/foret/mer"
        for i in range(1, 4):
            with open(f"{mer_path}/brigand_{i}.brig", "w") as f:
                f.write("Un brigand menaçant se tient devant toi.")
        print("Je pars pour la mer. Retrouve-moi là-bas, héros ! Les brigands rôdent sur la plage...")

        

class KingBrigandsManual(QuestValidation):  # Quest giver: Roi, Location: mer
    def validate_quest(self):
        super().validate_quest()
        mer_path = f"{base}/foret/mer"

        brigands = [
            os.path.join(mer_path, "brigand_1.brig"),
            os.path.join(mer_path, "brigand_2.brig"),
            os.path.join(mer_path, "brigand_3.brig"),
        ]
        if all(not os.path.exists(b) for b in brigands):
            return True, "Bravo, tu as terrassé ces brigands un par un ! Mais d'autres vont arriver en masse..."
        else:
            return False, "Il reste encore des brigands sur la plage, élimine-les !"
    def post_quest(self):
        mer_path = f"{base}/foret/mer"
        super().post_quest()
        for i in range(1, 101):
            with open(f"{mer_path}/brigand_{i}.brig", "w") as f:
                f.write("Un brigand menaçant se tient devant toi.")
        with open(f"{mer_path}/canon.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# /!\ ATTENTION : cette commande détruit TOUT dans le répertoire courant\n")
            f.write("rm *\n")
        os.chmod(f"{mer_path}/canon.sh", 0o600)

class KingCanonIntro(QuestValidation):  # Quest giver: Roi, Location: mer
    def validate_quest(self):
        super().validate_quest()
        mer_path = f"{base}/foret/mer"
        Roi_path = os.path.join(mer_path, "Roi.npc")

        Roi_vivant = os.path.exists(Roi_path)

        brigands_restants = [
            f for f in os.listdir(mer_path)
            if f.startswith("brigand_") and (f.endswith(".obj") or f.endswith(".brig"))
        ]
        plus_de_brigands = len(brigands_restants) == 0

        if Roi_vivant and plus_de_brigands:
            return True, "Victoire ! Les brigands ont été anéantis et je suis sauf. Le royaume est sauvé !"
        else:
            return False, "Les brigands ne sont pas tous éliminés, héros. Termine le travail !"

class IsKing(QuestValidation):
    def validate_quest(self):
        super().validate_quest()
        Roi_path = f"{base}/foret/mer/Roi.npc"
        if os.path.isfile(Roi_path):
            os.system(f"mv {base}/foret/mer/Roi.npc {base}/montagne/tunnel/route_de_montagne/vallee/chateau/")
            return True, "Ouf... tout va bien, il est là ! Mon coeur s'est arrêté... puis il a recommencé, de battre à nouveau. Sans lui, tout aurait sombré, mais sa présence éclaire encore nos ténèbres. Tant que le Roi respire, l'espoir du royaume vit encore ! \n BONNE FIN"
        else:
            return False, "Noooon... le Roi est mort ! Notre lumière s'est éteinte, et avec elle l'espoir du royaume... Qui nous protégera désormais des brigands et des tempêtes à venir ? Sans lui, le château n'est plus qu'un tombeau, et nous, de simples âmes perdues au milieu des ruines...\n MAUVAISE FIN"

class Story1(AlwaysValid): # Quest giver: Kevin, Location: village

    # Kevin says this after completing the mkdir quest.
    def post_quest(self):
        print(
            f"{self.npc} : Vous semblez très talentueux.\n"
            "Vous devriez explorer la forêt et la montagne, il y a des villageois qui pourraient avoir besoin de votre aide."
        )


class Story2(AlwaysValid): # Quest giver: Jacques, Location: mountain

    # Jacques says this after completing the move quest.
    def post_quest(self):
        print(
            f"{self.npc} : Merci de m'avoir aidé à retourner au village.\n"
            "Je voulais aller de l'autre côté de la montagne, mais je me suis cassé la jambe en essayant.\n"
            "Il était vraiment facile d'aller de l'autre côté de la montagne il y a quelques semaines, mais le raccourci a été détruit avec le village."
        )


class Story3(AlwaysValid): # Quest giver: Worker, Location: .secret_passage

    # Worker says this after completing the fedex1 quest.
    def post_quest(self):
        print(
            f"{self.npc} : Merci d'avoir apporté les outils !\n"
            "Je peux maintenant creuser un tunnel à travers la montagne jusqu'au village.\n"
            "Depuis que le raccourci a été détruit, il est vraiment difficile d'aller au château, beaucoup de villageois prennent des risques pour traverser la montagne."
        )


class Story4(AlwaysValid): # Quest giver: Merchant, Location: mountainroad

    # Merchant says this after completing the copy quest.
    def post_quest(self):
        print(
            f"{self.npc} : Merci d'avoir copié la bonne roue !\n"
            "Vous avez aidé à construire le tunnel à travers la montagne ? C'est génial ! Vous devriez aller au château, le Roi pourrait chercher quelqu'un comme vous."
        )

class Story5(AlwaysValid): # Quest giver: Quentintin, Location: Village

    def post_quest(self):
        print(
            f"{self.npc} : Je me sens si bien, caché de tous !\n"
            "Il parait qu'au fond du lac, il y'a un trésor, si tu arrives à trouver le Capitaine Haddock, parle lui, il te conseillera"
        )


MAP =  {
     "subzones": [
        {
            "name": "village",
            "npcs":
            [
                {
                    "name": "Kevin",
                    "talk": "Salut l'artiste ! Toujours prêt à bricoler ?",
                    "quests":
                    [
                        {
                            "name": "mkdir",
                            "must_done": [],
                            "text": "Le village est en ruines, nous devons le reconstruire. Pouvez-vous nous aider ? Utilisez la commande mkdir pour créer 3 répertoires (maisons) dans le village.",
                            "desc": "Aidez à reconstruire le village. Créez 3 maisons dans le village.",
                            "level": 1,
                            "script": "quests.npc_def.Mkdir",
                            "rewards": [
                                {
                                    "type": "command",
                                    "name": "cat <file>",
                                    "desc": "Lire le contenu d'un fichier",
                                },
                                {
                                    "type": "command",
                                    "name": "mkdir <dir>",
                                    "desc": "Créer un nouveau répertoire",
                                }
                            ]
                        },
                        {
                            "name": "story1",
                            "must_done": ["mkdir"],
                            "script": "quests.npc_def.Story1",
                            "desc": "Kevin vous dit que vous devriez explorer la forêt et la montagne, il y a des villageois qui pourraient avoir besoin de votre aide.",
                            "level": 0,
                            "rewards": [
                                {
                                    "type": "story",
                                    "value": "story1",
                                    "desc": "Kevin vous dit que vous devriez explorer la forêt et la montagne, il y a des villageois qui pourraient avoir besoin de votre aide.",
                                }
                            ],
                        }
                    ]
                },
                {
                    "name": "Quentintin",
                    "talk": "Chut... Tu veux pas qu'on me remarque, hein ?",
                    "quests":
                    [
                        {
                            "name": "Planque",
                            "must_done": ["mkdir", "list_hidden"],
                            "text": "Je n'aime pas me retrouver au milieu du village, cela m'angoisse, crée moi une planque par pitié",
                            "desc": "Aide moi à créer un dossier caché planque pour me cacher !",
                            "level": 1,
                            "script": "quests.npc_def.HiddenCreate"
                        },
                        {
                            "name": "Story5",
                            "must_done": ["Planque"],
                            "text": "Va trouver le capitaine haddock près du lac",
                            "desc": "Trouver Haddock",
                            "level": 1,
                            "script": "quests.npc_def.Story5"
                        }
                    ]
                },
                {
                    "name": "Paul",
                    "talk": "Yo ! C'est moi, Paul, le roi des combines.",
                    "quests":
                    [
                        {
                            "name": "who_s_there",
                            "must_doing": ["fedex1"],
                            "text": "Vous voulez des outils pour créer un tunnel à travers la montagne ? Bien sûr, mais d'abord, vous devez me donner votre nom.",
                            "desc": "Donnez votre nom à Paul.",
                            "level": 1,
                            "script": "quests.npc_def.WhoIsThere",
                            "rewards": [
                                {
                                    "type": "command",
                                    "name": "sort <fichier> -o <fichier>",
                                    "desc": "Permet de trier les lignes d'un fichier par ordre alphabétique",
                                },
                            ]
                        },
                    ]
                }
            ]
        },
        {
            "name": "montagne",  # mountain
            "npcs":
            [
                {
                    "name": "Jacques",
                    "talk": "Ouille... Ma jambe me fait souffrir, mais j'ai toujours le sourire !",
                    "quests":
                    [
                        {
                            "name": "move",
                            "must_done": [],
                            "text": "J'ai une jambe cassée. S'il vous plaît, aidez-moi à retourner au village.",
                            "desc": "Aidez Jacques à retourner au village.",
                            "level": 1,
                            "script": "quests.npc_def.Move",
                            "rewards":
                            [
                                {
                                    "type": "command",
                                    "name": "ls -a",
                                    "desc": "Lister tous les fichiers dans le répertoire courant, y compris les fichiers cachés",
                                },
                            ]
                        },
                        {
                            "name": "story2",
                            "must_done": ["move"],
                            "script": "quests.npc_def.Story2",
                            "desc": "Jacques vous raconte qu'il y avait autrefois un raccourci à travers la montagne, mais il a été détruit avec le village.",
                            "level": 0,
                            "rewards": [
                                {
                                    "type": "story",
                                    "value": "story2",
                                    "desc": "Jacques vous raconte qu'il y avait autrefois un raccourci à travers la montagne, mais il a été détruit avec le village.",
                                },
                                {
                                    "type": "command",
                                    "name": "mkdir .<dir>",
                                    "desc": "Créer un répertoire caché (commençant par un point)",
                                }
                            ]
                        }
                    ]
                }
            ],
            "subzones": [
                {
                    "name": ".passage_secret",  # .secret_passage
                    "must_done": ["list_hidden"],
                    "post_creation": lambda _: os.chmod(_, 0o600), # Must finishing the list_hidden quest to access this zone.
                    "npcs":
                    [
                        {
                            "name": "Ouvrier",
                            "talk": "Travail, boulot, sueur... Mais toujours avec le sourire !",
                            "quests":
                            [
                                {
                                    "name": "fedex1",
                                    "must_done": [],
                                    "text": "Je veux que vous alliez au village et que vous m'apportiez des outils pour faire un tunnel à travers la montagne, demandez au villageois nommé Paul.npc.",
                                    "desc": "Apportez des outils du village au passage secret.",
                                    "level": 2,
                                    "script": "quests.npc_def.Fedex1",
                                    "setup_quest": "quests.npc_def.SetupFedex1",
                                    "rewards": [
                                        {
                                            "type": "command",
                                            "name": "whoami",
                                            "desc": "Afficher le nom de l'utilisateur actuel",
                                        },
                                    ]
                                },
                                {
                                    "name": "story3",
                                    "must_done": ["fedex1"],
                                    "script": "quests.npc_def.Story3",
                                    "desc": "L'ouvrier vous dit qu'un nouveau tunnel est disponible pour aller de l'autre côté de la montagne.",
                                    "level": 0,
                                    "rewards": [
                                        {
                                            "type": "command",
                                            "name": "cp <source> <destination>",
                                            "desc": "Permet de copier un fichier",
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "subzones": [
                        {
                            "name": "route_de_montagne",  # mountainroad
                            "post_creation": lambda _: os.chmod(_, 0o600), # Must finishing the fedex1 quest to access this zone. // FIXME: Permissions are reset after fedex1 quest 
                            "npcs":
                            [
                                {
                                    "name": "Marchand",
                                    "talk": "Bienvenue, voyageur ! Mes affaires sont aussi variées que mes histoires.",
                                    "quests":
                                    [
                                        {
                                            "name": "copy",
                                            "must_done": [],
                                            "text": "Une des roues de ma charrette est cassée, l'autre est en bon état. Pouvez-vous faire une copie de la bonne roue ?",
                                            "desc": "Aidez le marchand en copiant le contenu de la bonne roue.",
                                            "level": 2,
                                            "script": "quests.npc_def.Copy",
                                        },
                                        {
                                            "name": "story4",
                                            "must_done": ["copy"],
                                            "script": "quests.npc_def.Story4",
                                            "desc": "Le marchand vous dit que vous devriez aller au château, le Roi pourrait chercher quelqu'un comme vous.",
                                            "level": 0,
                                            "rewards": []
                                        }
                                    ]
                                }
                            ],
                            "objects": [
                                {
                                    "name": "roue",  # wheel
                                    "desc": "Une roue parfaitement fonctionnelle provenant de la charrette d'un marchand.",
                                    "content": "a312cb11576b058d0b9a13e1c06c61ac"
                                }
                            ],
                            "subzones": [
                                {
                                    "name": "lac",  # lake
                                    "subzones": [
                                        {
                                            "name": "mer",  # sea
                                            "symlink_to": "foret/mer",  # forest/sea
                                        },
                                        {
                                            "name": "fond_du_lac",  # Fond du lac
                                            "npcs": [],
                                            "objects": [
                                                *create_lake_files() 
                                            ]
                                        }
                                    ],
                                    "npcs": [
                                        {
                                            "name": "Haddock",
                                            "talk": "Nom d'un tonnerre ! Approche, moussaillon, et écoute bien !",
                                            "quests": [
                                                {
                                                "name": "Find treasure",
                                                "must_done": ["Planque"],
                                                "text": "Mille milliards de tonnerres de Brest ! Ramenez ce maudit trésor du fond du lac... au lac ! Pas à la cave, pas au grenier, au lac, triple buse !",
                                                "desc": "Ramenez le trésor pour le capitaine Haddock",
                                                "level": 2,
                                                "script": "quests.npc_def.Treasure"
                                                },
                                                {
                                                "name": "Open treasure",
                                                "must_done": ["Find treasure"],
                                                "text": "Mille sabords ! Voilà le trésor empaqueté dans ce maudit .tar !\n\n Pour l'ouvrir, bande de bachibouzouks, tapez donc : tar -xvf tresor.tar \n...et que le butin se déverse enfin !",
                                                "desc": "Ramenez le trésor pour le capitaine Haddock",
                                                "level": 2,
                                                "script": "quests.npc_def.TreasureOpen"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "vallee",  # valley
                                    "npcs": [],
                                    "objects": [],
                                    "subzones": [
                                        {
                                            "name": "chateau",  # castle
                                            "npcs": [
                                                {
                                                    "name": "Serviteur",
                                                    "talk": "Bienvenue au château, noble invité. Puis-je vous aider ?",
                                                    "quests": [
                                                        {
                                                            "name": "sort_books",
                                                            "must_done": [],
                                                            "text": "Désolé, mais je ne peux pas vous guider dans le château, je dois trier les livres dans la bibliothèque.",
                                                            "desc": "Trier les livres dans la bibliothèque du château.",
                                                            "level": 2,
                                                            "script": "quests.npc_def.SortBooks"
                                                        },
                                                        {
                                                            "name": "Is_king",
                                                            "must_done": ["brigands_phase2"],
                                                            "text": "Bravo vous avez tué les brigands ! Mais où est notre Roi ?",
                                                            "desc": "Le Roi est-il mort ?.",
                                                            "level": 2,
                                                            "script": "quests.npc_def.IsKing"
                                                        }
                                                    ]
                                                }
                                            ],
                                            "subzones": [
                                                {
                                                    "name": "bibliotheque",  # library
                                                    "objects": [
                                                        {
                                                            "name": "livres",  # book
                                                            "desc": "Des livres qui doivent être trié.",
                                                            "content": "\n".join(livres) + "\n"
                                                        }
                                                    ],
                                                },
                                                {
                                                    "name": "donjon",  # dungeon
                                                    "npcs": [
                                                        {
                                                            "name": "Garde",
                                                            "talk": "Silence ! Je veille sur ce donjon, rien ne m'échappe.",
                                                            "quests": [
                                                                {
                                                                    "name": "shortcut",
                                                                    "must_done": ["sort_books"],
                                                                    "text": "J'ai besoin d'un raccourci vers le village, pouvez-vous en créer un ?",
                                                                    "desc": "Créer un raccourci vers le village.",
                                                                    "level": 3,
                                                                    "script": "quests.npc_def.shortcut"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "name": "salle_du_trone",
                                                    "npcs": [
                                                            {
                                                                "name": "Roi",
                                                                "talk": "Approche, héros. Le royaume a besoin de ton courage.",
                                                                "quests": [
                                                                    {
                                                                        "name": "royal_summons",
                                                                        "must_done": [],
                                                                        "text": "Enfin, te voilà. Des brigands venu détruire le royaume vont arriver par la mer ! Il faut y remédier.",
                                                                        "desc": "Parler au Roi",
                                                                        "level": 0,
                                                                        "script": "quests.npc_def.KingSummons",
                                                                        "rewards": []
                                                                    },
                                                                    {
                                                                        "name": "brigands_phase1",
                                                                        "must_done": ["royal_summons"],
                                                                        "text": "Élimine les 3 brigands sur la plage. Supprime-les un par un à la main.",
                                                                        "desc": "Vaincre 3 brigands manuellement.",
                                                                        "level": 2,
                                                                        "script": "quests.npc_def.KingBrigandsManual",
                                                                        "rewards": [
                                                                            {
                                                                                "type": "command",
                                                                                "name": "./canon.sh",
                                                                                "desc": "Faire tirer le canon"
                                                                            }
                                                                        ]
                                                                    },
                                                                    {
                                                                        "name": "brigands_phase2",
                                                                        "must_done": ["brigands_phase1"],
                                                                        "text": "Bien joué, mais ils reviennent par vagues ! Je te confie le canon.sh. Attention il peut s'avérer dangereux",
                                                                        "desc": "Vaincre tout les brigands",
                                                                        "level": 3,
                                                                        "script": "quests.npc_def.KingCanonIntro",
                                                                        "rewards": []
                                                                    }
                                                                ]
                                                            }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                    ]
                }
            ],
        },
        {
            "name": "foret",  # forest
            "npcs":
            [
                {
                    "name": "Alain_Leflou",
                    "talk": "Oups, j'ai encore perdu mes lunettes... Tu peux m'aider ?",
                    "quests":
                    [
                        {
                            "must_done": [],
                            "name": "list_read",
                            "text": "J'ai perdu mes lunettes, pouvez-vous lire le panneau pour moi afin que je puisse retourner au village ?",
                            "desc": "Lisez le panneau dans la forêt.",
                            "level": 1,
                            "script": "quests.npc_def.ReadFile",
                            "rewards":
                            [
                                {
                                    "type": "command",
                                    "name": "mv <source> <destination>",
                                    "desc": "Déplacer un fichier de la source à la destination",
                                },
                            ]
                        },
                        {
                            "must_done": ["list_read"],
                            "name": "list_hidden",
                            "text": "Il y a une carte au trésor cachée dans la forêt.",
                            "desc": "Trouvez et lisez le panneau caché dans la forêt.",
                            "level": 2,
                            "script": "quests.npc_def.HiddenFile",
                            "rewards":
                            [
                                {
                                    "type": "command",
                                    "name": "pwd",
                                    "desc": "Afficher le répertoire courant (le nom de la zone où vous vous trouvez actuellement)",
                                },
                            ]
                        }
                    ]
                },
            ],
            "objects":
            [
                {
                    "name": "panneau",  # sign
                    "desc": "Un panneau en bois avec du texte dessus.",
                    "content": "cd ../village\n"
                },
                {
                    "name": ".carte_cachee",  # .hidden_sign
                    "desc": "Une carte cachée avec du texte dessus.",
                    "content": "cd ../montagne/.passage_secret\n"
                }
            ],
            "subzones": [
                {
                    "name": "mer",  # sea
                    "npcs": [
                        {
                            "name": "Pecheur",
                            "talk": "Le vent, les vagues... et mes histoires de coquillages !",
                            "quests": [
                                {
                                    "name": "collect_shells",
                                    "must_done": [],
                                    "text": "J'ai trouvé un joli coquillage, mais je n'en ai pas besoin. Je peux vous le donner si vous le voulez.",
                                    "desc": "Obtenez le joli coquillage du pêcheur.",
                                    "level": 1,
                                    "script": "quests.npc_def.AcceptShell",
                                    "rewards": [
                                        {
                                            "type": "command",
                                            "name": "nom@machine:directory$ ",
                                            "desc": "Vous avez maintent un prompt qui vous indique votre nom d'utilisateur, le nom de la machine et le répertoire courant.",
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                }
            ]
        }
    ],
}


symlinks = []
post_ops = []
total_quests = 0
def create_zone(name, map_data):
    global symlinks
    global post_ops
    global total_quests
    for npcs in map_data.get("npcs", []):
        print(f"Creating NPC: {npcs['name']} in {name}")
        npc_path = os.path.join(name, f"{npcs['name'].lower().capitalize()}.npc")
        total_quests += len(npcs.get("quests", [])) 
        with open(npc_path, 'w') as npc_file:
            json.dump(npcs, npc_file, indent=4)
        print(f"Created NPC file at {npc_path}")
    for obj in map_data.get("objects", []):
        print(f"Creating object: {obj['name']} in {name}")
        obj_path = os.path.join(name, f"{obj['name'].lower()}.obj")
        with open(obj_path, 'w') as obj_file:
            obj_file.write(obj['content'])
        print(f"Created object file at {obj_path}")
    for subzone in map_data.get("subzones", []):
        if subzone.get("name", None) is None:
            continue
        print(f"Creating subzone: {subzone['name']} in {name}")
        subzone_path = os.path.join(name, subzone['name'])
        symlink = subzone.get("symlink_to", None)
        if symlink:
            symlinks.append((subzone_path, symlink))
        else:
            print(f"Creating directory for subzone {subzone['name']}")
            os.makedirs(subzone_path, exist_ok=True)
            post_creation = subzone.get("post_creation", None)
            if (post_creation):
                post_ops.append((post_creation, subzone_path))
            create_zone(subzone_path, subzone)


def create_symlinks(base_dir):
    for link, target in symlinks:
        link_path = os.path.join(base_dir, link)
        target_path = os.path.join(base_dir, target)
        if not os.path.exists(target_path):
            print(f"Target {target_path} does not exist for symlink {link_path}, skipping.")
            continue
        try:
            os.symlink(target_path, link_path)
            print(f"Created symlink: {link_path} -> {target_path}")
        except FileExistsError:
            print(f"Symlink {link_path} already exists, skipping.")
        except Exception as e:
            print(f"Error creating symlink {link_path}: {e}")

def execute_post_ops():
    for func, arg in post_ops:
        try:
            func(arg)
            print(f"Executed post operation {func} on {arg}")
        except Exception as e:
            print(f"Error executing post operation on {arg}: {e}")

def dump_map(json_data):
    with open("game_map.json", 'w') as f:
        json.dump(json_data, f, indent=4)
    print("Game map dumped to game_map.json")




if __name__ == "__main__":
    #dump_map(MAP)
    base_dir = os.path.join("/tmp", "game_map")
    os.system(f"rm -rf {base_dir}")  # temp. cleanup
    os.makedirs(base_dir)
    create_zone(base_dir, MAP)
    create_symlinks(base_dir)
    execute_post_ops()
    print(f"Game map created at {base_dir} with total quests: {total_quests}")

### REST OF THE LORE IDEA:

"""
Speak to the King, he seems very young but he seems to recognize you.

You ask him about the village destruction, he tells you that the village was destroyed by brigands who arrived by the sea a few weeks ago.

That night the King lost his father, the previous King who went to defend the village with his army and an inexperienced mage.

The mage knew some powerful spells but was not able to control them, he accidentally destroyed the village and killed the previous King and his army.

As you can also cast some spells, the King asks you to be his new mage and help him defend the continent against the brigands.

You get a quest to find the mage's spellbook, which is hidden in the depth of the lake.

You eventually find a chest in the lake containing the spellbook, but it is protected by a spell requiring you to solve a riddle:
- "The content of the chest will be available to people who are in the tux group."
- "The content of the chest will be available to people who can cast the decryption spell: gpg -a --decrypt --cipher-algo AES256 <file>"

Being tux also allows you to enter the mage's quarters in the castle, where you can train your magic skills and learn new spells.

You eventually solve the riddle and decrypt the spellbook, which contains powerful spells to help you defend the continent:
One day the King asks you to help him with the brigands, they are back (comming from the sea) and they are stronger than ever.
- rm <file>: to remove files -> Used to delete enemies files, but enemies will come back. (neutral ending)
  - Improved rm command: rm * -> to remove all files in the current directory including the new King (bad ending)
- chmod <permissions> <file>: to change file permissions -> Used to make a script executable, the script does a rm -rf /* on the continent (worst ending)
  - Improved script: edit the script to change the rm -rf / to a safer command like rm *.enemy (good ending)
- ps -ef and kill <pid>: to manage processes -> Used to find the enemy spawning process and kill it (best ending)
"""