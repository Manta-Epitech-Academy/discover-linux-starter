import os
import json
import shutil
import pwd
import random
import hashlib
import base64
from config import T
from treasure_base64 import treasure_base64
from translation_tab import *
import map
from path import *


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

def find_parent_in_dict(obj, key, value):
    """Recursively find parent dicts that contain a specific key/value."""
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Check for a match at this level
            if k == key and v == value:
                results.append(obj)
            # Recurse deeper
            results.extend(find_parent_in_dict(v, key, value))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_parent_in_dict(item, key, value))
    return results


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
        if Checks.get_subdir_count(village_path) >= 3:
            return True, f"Bravo ! Vous avez créé 3 maisons dans le {village[T]}."
        else:
            return False, f"Vous devez créer 3 maisons dans le {village[T]} en utilisant la commande mkdir."

class HiddenCreate(QuestValidation):  # Quest giver: Quentintin, Location: Village
    def validate_quest(self):
        super().validate_quest()
        hidden_dirs = [
            d for d in os.listdir(village_path)
            if d.startswith(".") and os.path.isdir(os.path.join(village_path, d))
        ]
        if hidden_dirs:
            hidden_path = os.path.join(village_path, hidden_dirs[0])
            os.system(f"mv {village_path}/Quentintin.npc {hidden_path}/")
            return True, f"Merci d'avoir créé une planque ({hidden_dirs[0]}) !"
        else:
            return False, "Crée-moi une planque (un dossier caché, commençant par '.')."

class Treasure(QuestValidation):
    def validate_quest(self):
        super().validate_quest()
        if os.path.isfile(f"{lac_path}/tresor.tar.obj"):
            os.system(f"mv {lac_path}/tresor.tar.obj {lac_path}/tresor.tar")
            return True, "Tonnerre de tonnerres ! Merci d'avoir repêché ce sacré trésor, mais maintenant, bougre d'explorateur d'eau douce, il va falloir l'ouvrir, nom d'un bachibouzouk !"
        else:
            return False, f"Mille sabords ! Halte-là, moussaillons ! Ramenez ce trésor au bercail, droit au {lake[T]}, et plus vite que ça, espèces de marins d'eau douce !"

class TreasureOpen(QuestValidation): # Quest giver: Haddock, Location: Lake
    def validate_quest(self):
        super().validate_quest()
        if os.path.isdir(f"{lac_path}/tresor"):
            return True, "Tonnerre de Brest ! Bravo, moussaillon, tu as ouvert le trésor ! Mille millions de sabords, te voilà désormais en possession des deux formules magiques... ça pourra te servir plus tard, ou que le diable m'emporte !"
        else:
            return False, f"Mille milliards de mille sabords ! N'oublie pas ta quête, moussaillon : ouvre le trésor et empare-toi des deux formules magiques, ou tu finiras marin d'eau douce à vie !"

class ReadFile(QuestValidation): # Quest giver: Kevin, Location: forest

    def validate_quest(self):
        super().validate_quest()
        if Checks.input_str(f"Veuillez lire le panneau pour moi : ") == f"cd ../{village[T]}":
            return True, "Merci d'avoir lu le panneau !"
        else:
            return False, f"Ce n'est pas ce qui est écrit sur le panneau ! Veuillez réessayer."

class WhoIsThere(QuestValidation): # Quest giver: Paul, Location: village

    def validate_quest(self):
        super().validate_quest()
        if Checks.input_str("Veuillez me donner votre nom : ") == pwd.getpwuid(os.getuid()).pw_name:
            with open(f"{village_path}/outils.obj", 'w') as f:
                f.write("c047eaea91e27374")
            return True, "Merci de m'avoir donné votre nom !"
        else:
            return False, "Ce n'est pas votre nom ! Veuillez réessayer."

class Move(QuestValidation): # Quest giver: Jacques, Location: mountain

    def validate_quest(self):
        super().validate_quest()
        if Checks.file_under_location("Jacques.npc", village[T]) and not Checks.file_under_location("Jacques.npc", mountain[T]):
            return True, f"Enfin chez moi dans le {village[T]} !"
        else:
            return False, f"Veuillez m'aider à retourner au {village[T]}"

class Fedex1(QuestValidation): # Quest giver: Worker, Location: .passage_secret

    def validate_quest(self):
        super().validate_quest()
        if Checks.file_content_match(f"{passage_secret_path}/outils.obj", "c047eaea91e27374") or Checks.file_content_match(f"{tunnel_path}/outils.obj", "c047eaea91e27374"):
            return True, "Merci d'avoir apporté les outils !"
        else:
            return False, f"Vous devez apporter les outils du {village[T]} au passage secret."
    def post_quest(self):
        if os.path.isdir(passage_secret_path):
            os.rename(passage_secret_path, tunnel_path)
            os.chmod(route_de_montagne_path, 0o755)
            os.system(f"cd {montagne_path}; bash --norc")



class Copy(QuestValidation): # Quest giver: Merchant, Location: mountainroad

    def validate_quest(self):
        super().validate_quest()
        if Checks.has_duplicate_in_dir(f"{route_de_montagne_path}/roue.obj", f"{route_de_montagne_path}/"):
            return True, "Bravo ! Vous avez copié la bonne roue."
        else:
            return False, "Vous devez copier le contenu de la bonne roue."


class SortBooks(QuestValidation): # Quest giver: Servant, Location: castle

    def validate_quest(self):
        super().validate_quest()
        for file in os.listdir(bibliotheque_path):
            if file.endswith(".obj"):
                path = f"{bibliotheque_path}/{file}"
                attendu = "\n".join(sorted(livres)) + "\n"
                with open(path, "r") as f:
                    contenu = f.read()
                if contenu == attendu:
                    return True, "Merci d'avoir trié les livres !"
        return False, "Vous devez trier les livres dans la bibliothèque."


class Shortcut(QuestValidation): # Quest giver: Guard, Location: dungeon

    def validate_quest(self):
        super().validate_quest()
        dungeon_path = f"{base}/{donjon_path}"
        symlink_to_village = None
        for file in os.listdir(dungeon_path):
            abspath = f"/{dungeon_path}/{file}"
            if (os.path.exists(abspath) and os.path.islink(abspath) and os.path.isdir(abspath)):
                try:
                    original_path = os.readlink(abspath)
                    if os.path.samefile(original_path, f"/{base}/{village_path}"):
                        symlink_to_village = abspath
                        break
                except:
                    continue
        if symlink_to_village:
            return True, f"Vous avez créé un raccourci vers le {village_path} !"
        else:
            return False, f"Vous devez créer un raccourci vers le {village_path}."


class HiddenFile(QuestValidation): # Quest giver: Kevin, Location: forest

    def validate_quest(self):
        super().validate_quest()
        with open(f"{base}/{forest[T]}/.carte_cachee.obj", "r") as f:
            file_content = f.read().strip()
        if Checks.input_str("Quel est le contenu de la carte du passage secret ?") == file_content:
            self.post_quest()
            return True, "Vous avez trouvé la carte du passage secret !"
        else:
            return False, "Vous devez trouver la carte du passage secret dans la forêt."

    def post_quest(self):
        try:
            os.chmod(f"{passage_secret_path}", 0o755)
            os.chmod(f"{route_de_montagne_path}", 0o600)
        except:
            pass


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
            f"mv {throne_room}/Roi.npc {mer_for_path}/"
        )
        mer_path = f"{mer_for_path}"
        for i in range(1, 4):
            with open(f"{mer_path}/brigand_{i}.brig", "w") as f:
                f.write("Un brigand menaçant se tient devant toi.")
        print(f"Je pars pour la {sea[T]}. Retrouve-moi là-bas, héros ! Les brigands rôdent sur la plage...")

        

class KingBrigandsManual(QuestValidation):  # Quest giver: Roi, Location: mer
    def validate_quest(self):
        super().validate_quest()

        brigands = [
            os.path.join(mer_for_path, "brigand_1.brig"),
            os.path.join(mer_for_path, "brigand_2.brig"),
            os.path.join(mer_for_path, "brigand_3.brig"),
        ]
        if all(not os.path.exists(b) for b in brigands):
            return True, "Bravo, tu as terrassé ces brigands un par un ! Mais d'autres vont arriver en masse..."
        else:
            return False, "Il reste encore des brigands sur la plage, élimine-les !"
    def post_quest(self):
        super().post_quest()
        for i in range(1, 101):
            with open(f"{mer_for_path}/brigand_{i}.brig", "w") as f:
                f.write("Un brigand menaçant se tient devant toi.")
        with open(f"{mer_for_path}/canon.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# /!\ ATTENTION : cette commande détruit TOUT dans le répertoire courant\n")
            f.write("rm *\n")
        os.chmod(f"{mer_for_path}/canon.sh", 0o600)

class KingCanonIntro(QuestValidation):  # Quest giver: Roi, Location: mer
    def validate_quest(self):
        super().validate_quest()
        Roi_path = os.path.join(mer_for_path, "Roi.npc")

        Roi_vivant = os.path.exists(Roi_path)

        brigands_restants = [
            f for f in os.listdir(mer_for_path)
            if f.startswith("brigand_") and (f.endswith(".obj") or f.endswith(".brig"))
        ]
        plus_de_brigands = len(brigands_restants) == 0

        if Roi_vivant and plus_de_brigands:
            return True, "Victoire ! Les brigands ont été anéantis et je suis sauf. Le royaume est sauvé !"
        else:
            return False, "Les brigands ne sont pas tous éliminés, héros. Termine le travail !"

    def post_quest(self):
        with open("/tmp/chef_brigand", "w") as f:
            f.write(f"""
            #!/bin/bash
            while true; do
                NB_BRIG=`ls -l {mer_for_path} | grep -c '.brig'`
                [[ $NB_BRIG -lt 10 ]] && echo "Un brigand menaçant se tient devant toi." > brigand_$RANDOM.brig
                sleep $(($(($RANDOM % 10)) + 1))
            done
            """)
        os.system("chmod +x /tmp/chef_brigand")
        os.system("pgrep chef_brigand || /tmp/chef_brigand &")

class KillProcess(QuestValidation):
    def validate_quest(self):
        if os.system("pgrep chef_brigand") != 0:
            return True, "Le chef des brigands n'est plus là. Victoire !"
        else:
            return False, "Le chef des brigands est toujours là... Trouve son processus et arrête-le !"

class IsKing(QuestValidation):
    def validate_quest(self):
        super().validate_quest()
        Roi_path = f"{mer_for_path}/Roi.npc"
        if os.path.isfile(Roi_path):
            os.system(f"mv {mer_for_path}/Roi.npc {chateau_path}/")
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
            f"{self.npc} : Merci de m'avoir aidé à retourner au {village[T]}.\n"
            "Je voulais aller de l'autre côté de la montagne, mais je me suis cassé la jambe en essayant.\n"
            f"Il était vraiment facile d'aller de l'autre côté de la montagne il y a quelques semaines, mais le raccourci a été détruit avec le {village[T]}."
        )


class Story3(AlwaysValid): # Quest giver: Worker, Location: .secret_passage

    # Worker says this after completing the fedex1 quest.
    def post_quest(self):
        print(
            f"{self.npc} : Merci d'avoir apporté les outils !\n"
            f"Je peux maintenant creuser un tunnel à travers la montagne jusqu'au {village[T]}.\n"
            "Depuis que le raccourci a été détruit, il est vraiment difficile d'aller au château, beaucoup de villageois prennent des risques pour traverser la montagne."
        )


class Story4(AlwaysValid): # Quest giver: Merchant, Location: mountainroad

    # Merchant says this after completing the copy quest.
    def post_quest(self):
        print(
            f"{self.npc} : Merci d'avoir copié la bonne roue !\n"
            f"Vous avez aidé à construire le tunnel à travers la montagne ? C'est génial ! Vous devriez aller au {castle[T]}, le Roi pourrait chercher quelqu'un comme vous."
        )

class Story5(AlwaysValid): # Quest giver: Quentintin, Location: Village

    def post_quest(self):
        print(
            f"{self.npc} : Je me sens si bien, caché de tous !\n"
            f"Il parait qu'au fond du {lake[T]}, il y'a un trésor, si tu arrives à trouver le Capitaine Haddock, parle lui, il te conseillera"
        )

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
    create_zone(base_dir, map.MAP)
    create_symlinks(base_dir)
    execute_post_ops()
    print(f"Game map created at {base_dir} with total quests: {total_quests}")

