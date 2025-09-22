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


MAP_HALLOWEEN = {
     "subzones": [
        {
            "name": "village",
            "npcs":
            [
                {
                    "name": "Kevin",
                    "talk": "Bouh ! Me revoilà, artisan de l’ombre… Prêt à relever les ruines hantées ?",
                    "quests":
                    [
                        {
                            "name": "mkdir",
                            "must_done": [],
                            "text": "Le village est devenu un cimetière de ruines… nous devons le relever avant que les spectres ne s’en emparent ! Utilisez la commande mkdir pour ériger 3 maisons (abris contre les esprits).",
                            "desc": "Aidez à reconstruire le village hanté. Créez 3 maisons pour repousser les fantômes.",
                            "level": 1,
                            "script": "quests.npc_def.Mkdir",
                            "rewards": [
                                {
                                    "type": "command",
                                    "name": "cat <file>",
                                    "desc": "Lire les sombres secrets gravés dans un fichier",
                                },
                                {
                                    "type": "command",
                                    "name": "mkdir <dir>",
                                    "desc": "Invoquer une nouvelle demeure à partir du néant",
                                }
                            ]
                        },
                        {
                            "name": "story1",
                            "must_done": ["mkdir"],
                            "script": "quests.npc_def.Story1",
                            "desc": "Kevin vous murmure qu’il faudrait explorer la forêt maudite et la montagne obscure… des âmes perdues y attendent votre aide.",
                            "level": 0,
                            "rewards": [
                                {
                                    "type": "story",
                                    "value": "story1",
                                    "desc": "Kevin vous murmure qu’il faudrait explorer la forêt maudite et la montagne obscure… des âmes perdues y attendent votre aide.",
                                }
                            ],
                        }
                    ]
                },
                {
                    "name": "Quentintin",
                    "talk": "Chhhht… Les esprits rôdent, tu ne veux pas qu’ils m’entendent, si ?",
                    "quests":
                    [
                        {
                            "name": "Planque",
                            "must_done": ["mkdir", "list_hidden"],
                            "text": "Je déteste rester au milieu du village… les lanternes dansent et les ombres m’étranglent. Crée-moi une cachette, je t’en supplie !",
                            "desc": "Aidez Quentintin à créer un repaire secret, un dossier caché où il pourra se dissimuler des spectres.",
                            "level": 1,
                            "script": "quests.npc_def.HiddenCreate"
                        },
                        {
                            "name": "Story5",
                            "must_done": ["Planque"],
                            "text": "Trouve le capitaine Haddock près du lac maudit, il t’attend dans le brouillard.",
                            "desc": "Rejoins Haddock au bord du lac hanté.",
                            "level": 1,
                            "script": "quests.npc_def.Story5"
                        }
                    ]
                },
                {
                    "name": "Paul",
                    "talk": "Ahahah ! C’est moi, Paul, le marchand de malices et de lanternes ensorcelées.",
                    "quests":
                    [
                        {
                            "name": "who_s_there",
                            "must_doing": ["fedex1"],
                            "text": "Tu veux des outils pour creuser un passage dans la montagne des damnés ? Donne-moi d’abord ton nom, mortel…",
                            "desc": "Révélez votre nom à Paul, le filou des ténèbres.",
                            "level": 1,
                            "script": "quests.npc_def.WhoIsThere",
                            "rewards": [
                                {
                                    "type": "command",
                                    "name": "sort <fichier> -o <fichier>",
                                    "desc": "Trier des lignes… ou des incantations, par ordre alphabétique.",
                                },
                            ]
                        },
                    ]
                }
            ]
        },
        {
            "name": "montagne",
            "npcs":
            [
                {
                    "name": "Jacques",
                    "talk": "Aïe… ma jambe me ronge comme une malédiction, mais je garde le sourire du squelette !",
                    "quests":
                    [
                        {
                            "name": "move",
                            "must_done": [],
                            "text": "Ma jambe est brisée… Aidez-moi à regagner le village avant que les goules ne viennent me chercher.",
                            "desc": "Ramenez Jacques au village avant que les ombres n’approchent.",
                            "level": 1,
                            "script": "quests.npc_def.Move",
                            "rewards":
                            [
                                {
                                    "type": "command",
                                    "name": "ls -a",
                                    "desc": "Révéler tout ce qui se cache dans les ténèbres, y compris l’invisible…",
                                },
                            ]
                        },
                        {
                            "name": "story2",
                            "must_done": ["move"],
                            "script": "quests.npc_def.Story2",
                            "desc": "Jacques vous raconte qu’il existait jadis un sombre passage à travers la montagne… détruit quand les flammes ont dévoré le village.",
                            "level": 0,
                            "rewards": [
                                {
                                    "type": "story",
                                    "value": "story2",
                                    "desc": "Jacques vous raconte qu’il existait jadis un sombre passage à travers la montagne… détruit quand les flammes ont dévoré le village.",
                                },
                                {
                                    "type": "command",
                                    "name": "mkdir .<dir>",
                                    "desc": "Créer un repaire secret (un répertoire invisible, marqué par un point).",
                                }
                            ]
                        }
                    ]
                }
            ],
            "subzones": [
                {
                    "name": ".passage_secret",
                    "must_done": ["list_hidden"],
                    "post_creation": lambda _: os.chmod(_, 0o600),
                    "npcs":
                    [
                        {
                            "name": "Ouvrier",
                            "talk": "Travail sans fin… mes mains couvertes de poussière et de sang. Mais je souris toujours, même dans l’ombre !",
                            "quests":
                            [
                                {
                                    "name": "fedex1",
                                    "must_done": [],
                                    "text": "Apportez-moi des outils du village… sinon, nous resterons prisonniers dans cette montagne maudite. Cherchez Paul, le fourbe aux lanternes.",
                                    "desc": "Apportez des outils du village au passage secret.",
                                    "level": 2,
                                    "script": "quests.npc_def.Fedex1",
                                    "setup_quest": "quests.npc_def.SetupFedex1",
                                    "rewards": [
                                        {
                                            "type": "command",
                                            "name": "whoami",
                                            "desc": "Révéler le nom de l’âme qui habite ce corps.",
                                        },
                                    ]
                                },
                                {
                                    "name": "story3",
                                    "must_done": ["fedex1"],
                                    "script": "quests.npc_def.Story3",
                                    "desc": "L’ouvrier vous dit qu’un tunnel hanté est désormais ouvert, menant de l’autre côté de la montagne.",
                                    "level": 0,
                                    "rewards": [
                                        {
                                            "type": "command",
                                            "name": "cp <source> <destination>",
                                            "desc": "Copier un objet… ou une malédiction.",
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "subzones": [
                        {
                            "name": "route_de_montagne",
                            "post_creation": lambda _: os.chmod(_, 0o600),
                            "npcs":
                            [
                                {
                                    "name": "Marchand",
                                    "talk": "Bienvenue, voyageur… mes marchandises grincent autant que mes histoires lugubres.",
                                    "quests":
                                    [
                                        {
                                            "name": "copy",
                                            "must_done": [],
                                            "text": "Une roue de ma charrette spectrale est brisée. L’autre est intacte… pouvez-vous en faire une copie avant que le sortilège ne s’effondre ?",
                                            "desc": "Aidez le marchand en copiant la roue encore intacte.",
                                            "level": 2,
                                            "script": "quests.npc_def.Copy",
                                        },
                                        {
                                            "name": "story4",
                                            "must_done": ["copy"],
                                            "script": "quests.npc_def.Story4",
                                            "desc": "Le marchand vous glisse qu’au château, un Roi en quête de héros vous attend dans les ténèbres.",
                                            "level": 0,
                                            "rewards": []
                                        }
                                    ]
                                }
                            ],
                            "objects": [
                                {
                                    "name": "roue",
                                    "desc": "Une roue grinçante mais intacte, sortie d’une charrette spectrale.",
                                    "content": "a312cb11576b058d0b9a13e1c06c61ac"
                                }
                            ],
                            "subzones": [
                                {
                                    "name": "lac",
                                    "subzones": [
                                        {
                                            "name": "mer",
                                            "symlink_to": "foret/mer",
                                        },
                                        {
                                            "name": "fond_du_lac",
                                            "npcs": [],
                                            "objects": [
                                                *create_lake_files() 
                                            ]
                                        }
                                    ],
                                    "npcs": [
                                        {
                                            "name": "Haddock",
                                            "talk": "Par les abysses et les spectres marins ! Approche, moussaillon des ombres…",
                                            "quests": [
                                                {
                                                "name": "Find treasure",
                                                "must_done": ["Planque"],
                                                "text": "Ramène-moi ce trésor maudit qui dort au fond du lac noir… Et pas ailleurs, sombre crâne d’os !",
                                                "desc": "Ramenez le trésor pour le capitaine fantomatique Haddock.",
                                                "level": 2,
                                                "script": "quests.npc_def.Treasure"
                                                },
                                                {
                                                "name": "Open treasure",
                                                "must_done": ["Find treasure"],
                                                "text": "Ce coffre est enfermé dans un cercueil .tar ! Pour le briser : tar -xvf tresor.tar … et que les malédictions s’échappent enfin !",
                                                "desc": "Ouvrez le trésor pour Haddock.",
                                                "level": 2,
                                                "script": "quests.npc_def.TreasureOpen"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "vallee",
                                    "npcs": [],
                                    "objects": [],
                                    "subzones": [
                                        {
                                            "name": "chateau",
                                            "npcs": [
                                                {
                                                    "name": "Serviteur",
                                                    "talk": "Bienvenue dans le château aux couloirs glacés… Puis-je vous assister, hôte de l’ombre ?",
                                                    "quests": [
                                                        {
                                                            "name": "sort_books",
                                                            "must_done": [],
                                                            "text": "Pardonnez-moi, mais je dois trier ces grimoires poussiéreux avant de pouvoir vous guider.",
                                                            "desc": "Trier les grimoires de la bibliothèque du château.",
                                                            "level": 2,
                                                            "script": "quests.npc_def.SortBooks"
                                                        },
                                                        {
                                                            "name": "Is_king",
                                                            "must_done": ["brigands_phase2"],
                                                            "text": "Bravo… vous avez purgé les brigands. Mais notre Roi… est-il encore parmi les vivants ?",
                                                            "desc": "Le Roi est-il mort… ou pire ?",
                                                            "level": 2,
                                                            "script": "quests.npc_def.IsKing"
                                                        }
                                                    ]
                                                }
                                            ],
                                            "subzones": [
                                                {
                                                    "name": "bibliotheque",
                                                    "objects": [
                                                        {
                                                            "name": "livres",
                                                            "desc": "Des grimoires poussiéreux qui attendent d’être triés.",
                                                            "content": "\n".join(livres) + "\n"
                                                        }
                                                    ],
                                                },
                                                {
                                                    "name": "donjon",
                                                    "npcs": [
                                                        {
                                                            "name": "Garde",
                                                            "talk": "Silence ! Dans ce donjon hanté, rien n’échappe à mon regard de pierre.",
                                                            "quests": [
                                                                {
                                                                    "name": "shortcut",
                                                                    "must_done": ["sort_books"],
                                                                    "text": "J’ai besoin d’un raccourci vers le village… sinon je serai damné à garder cette porte à jamais.",
                                                                    "desc": "Créer un raccourci spectral vers le village.",
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
                                                                "talk": "Approche, héros des ténèbres… le royaume agonise, et ton courage est notre dernière lueur.",
                                                                "quests": [
                                                                    {
                                                                        "name": "royal_summons",
                                                                        "must_done": [],
                                                                        "text": "Enfin, te voilà. Des brigands sortis des abysses arrivent par la mer ! Ils doivent être détruits.",
                                                                        "desc": "Parler au Roi spectral.",
                                                                        "level": 0,
                                                                        "script": "quests.npc_def.KingSummons",
                                                                        "rewards": []
                                                                    },
                                                                    {
                                                                        "name": "brigands_phase1",
                                                                        "must_done": ["royal_summons"],
                                                                        "text": "Élimine les 3 brigands de la plage… tranche-les à la main, un par un, avant que la lune ne se voile.",
                                                                        "desc": "Vaincre 3 brigands manuellement.",
                                                                        "level": 2,
                                                                        "script": "quests.npc_def.KingBrigandsManual",
                                                                        "rewards": [
                                                                            {
                                                                                "type": "command",
                                                                                "name": "./canon.sh",
                                                                                "desc": "Déchaîner la colère du canon maudit",
                                                                            }
                                                                        ]
                                                                    },
                                                                    {
                                                                        "name": "brigands_phase2",
                                                                        "must_done": ["brigands_phase1"],
                                                                        "text": "Bien joué… mais les vagues en amènent d’autres ! Prends ce canon.sh, mais prends garde : il est aussi dangereux qu’instable.",
                                                                        "desc": "Vaincre la horde entière de brigands.",
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
            "name": "foret",
            "npcs":
            [
                {
                    "name": "Alain_Leflou",
                    "talk": "Oh non… j’ai encore perdu mes lunettes ! Sans elles, les esprits du bois me guettent… peux-tu m’aider ?",
                    "quests":
                    [
                        {
                            "must_done": [],
                            "name": "list_read",
                            "text": "Mes yeux aveugles ne peuvent lire le panneau maudit… lis-le pour moi, que je retrouve le chemin du village.",
                            "desc": "Lisez le panneau hanté dans la forêt.",
                            "level": 1,
                            "script": "quests.npc_def.ReadFile",
                            "rewards":
                            [
                                {
                                    "type": "command",
                                    "name": "mv <source> <destination>",
                                    "desc": "Déplacer un fichier… comme un spectre glissant dans l’ombre.",
                                },
                            ]
                        },
                        {
                            "must_done": ["list_read"],
                            "name": "list_hidden",
                            "text": "Une carte au trésor maudit est tapie dans la forêt, cachée aux yeux des vivants.",
                            "desc": "Trouvez et lisez le panneau spectral dissimulé dans la forêt.",
                            "level": 2,
                            "script": "quests.npc_def.HiddenFile",
                            "rewards":
                            [
                                {
                                    "type": "command",
                                    "name": "pwd",
                                    "desc": "Révéler la crypte (le répertoire courant où vous vous trouvez).",
                                },
                            ]
                        }
                    ]
                },
            ],
            "objects":
            [
                {
                    "name": "panneau",
                    "desc": "Un panneau en bois rongé par les toiles d’araignées, avec des symboles étranges.",
                    "content": "cd ../village\n"
                },
                {
                    "name": ".carte_cachee",
                    "desc": "Un parchemin moisi, caché sous les feuilles mortes, couvert de runes.",
                    "content": "cd ../montagne/.passage_secret\n"
                }
            ],
            "subzones": [
                {
                    "name": "mer",
                    "npcs": [
                        {
                            "name": "Pecheur",
                            "talk": "Le vent hurle, les vagues gémissent… et moi je ramasse des coquillages maudits.",
                            "quests": [
                                {
                                    "name": "collect_shells",
                                    "must_done": [],
                                    "text": "J’ai trouvé un coquillage aux reflets sinistres… mais il ne me servira à rien. Tu le veux ?",
                                    "desc": "Obtenez le coquillage maudit du pêcheur.",
                                    "level": 1,
                                    "script": "quests.npc_def.AcceptShell",
                                    "rewards": [
                                        {
                                            "type": "command",
                                            "name": "nom@machine:directory$ ",
                                            "desc": "Votre prompt révèle désormais votre nom d’utilisateur, le nom de la machine et la crypte (répertoire courant).",
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
    create_zone(base_dir, MAP_HALLOWEEN)
    create_symlinks(base_dir)
    execute_post_ops()
    print(f"Game map created at {base_dir} with total quests: {total_quests}")

