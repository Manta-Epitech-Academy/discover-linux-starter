#!/usr/bin/env python3

import os
import json
import sys
import importlib

PLAYER_FILE = '/tmp/player.json'

# Example player file content:
# {
#     "base_dir": "/tmp/", -> this is the root directory for the game
#     "quests": [
#         {"name": "mkdir", "desc": "Create 3 dir", "level": 1, "check": "quests.quest1.MkdirQuest"},
#         {"name": "move", "desc": "Help the NPC move to the village", "level": 1, "check": "quests.quest1.MoveQuest"}
#         {"name": "list_hiddden", "desc": "Find the hidden sign", "level": 2, "check": "quests.quest1.ListReadHiddenFile"}
#     ],
#     "quests_done": [
#         {"name": "list_read", "desc": "Read the sign", "level": 1, "check": "quests.quest1.ListReadFile"}
#     ]
# }


def bold(text):
    return f"\033[1m{text}\033[0m"

intro_story = {
    "type": "story",
    "desc": "Vous vous réveillez dans un endroit inconnu. Autour de vous, des chemins s'étendent dans plusieurs directions.\n"
    "    Vous vous levez et vous commencez à regarder autour de vous.\n"
    "    Utilisez la commande 'ls' (tapez 'ls' au clavier suivi de la touche Entrée) pour observer ce qui vous entoure.\n"
    "    Utilisez la commande 'cd <directory>' pour vous déplacer dans une direction (ex: cd village).\n"
    "    Utilisez la commande 'talk <npc>' pour parler à un PNJ (ex: talk toto.npc).\n",
    "value": "Introduction à l'aventure"
}

class Zone:
    def __init__(self):
        self.name = os.getcwd()
        self.list_dir = os.listdir(self.name)

    def list_npcs(self):
        self.npcs = [NPC(i) for i in os.listdir(self.name) if i.endswith('.npc')]
        return self.npcs

    def list_zones(self):
        self.subzones = [filter(os.path.isdir, self.list_dir)]

    def __repr__(self):
        return f"Zone(name={self.name}, npcs={self.npcs})"

class Quest:
    def __init__(self, name, desc, *args, **kwargs):
        self.name = name
        self.desc = desc
        self.level = kwargs["level"]

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_level(self):
        return self.level

    def __repr__(self):
        return f"  - {self.name}\n    Description={self.desc}" if self.level > 0 else ""

class Player:
    def __init__(self, *args, **kwargs):
        if not self.load():
            self.level = 1
            self.quests = []
            self.quests_done = []
            self.commands = [
                {"type": "command", "value": "talk", "desc": "Parler à un PNJ (ex: talk toto.npc)"},
                {"type": "command", "value": "player", "desc": "Afficher le statut du joueur"},
                {"type": "command", "value": "cd <directory>", "desc": "Changer de répertoire (changer de zone) (ex: cd village)"},
                {"type": "command", "value": "cd ..", "desc": "Remonter d'un répertoire (retourner à la zone précédente)"},
                {"type": "command", "value": "ls", "desc": "Lister les fichiers et répertoires (observer ce qui se trouve dans la zone) (ex: ls)"},
            ]
            self.stories = []
            if len(args) > 0:
                self.base_dir = args[0]
            elif 'base_dir' in kwargs:
                self.base_dir = kwargs['base_dir']
            else:
                raise ValueError("Base directory must be specified for Player initialization.")
            self.save()

    def get_quests(self):
        return self.quests

    def get_quests_done(self):
        return self.quests_done

    def get_all_quests(self):
        return self.quests + self.quests_done

    def add_quest(self, quest):
        if quest not in self.quests and quest not in self.quests_done:
            if (quest.get('level', 0) > 0):
                print(bold(f"Nouvelle quête: {quest.get('name', None)} - {quest.get('desc', None)}"))
            self.quests.append(quest)
        self.save()

    def add_reward(self, rewards):
        for reward in rewards:
            if reward in self.commands or reward in self.stories:
                continue
            if reward.get('type') == 'command':
                if reward not in self.commands:
                    self.commands.append(reward)
                    print(bold(f"Nouvelle commande '{reward.get('name')}' apprise, utilisez la command 'player' pour voir la liste des commandes."))
            if reward.get('type') == 'story':
                self.stories.append(reward)
                print(bold(f"Nouvelle histoire débloquée, utilisez la command 'player' pour voir l'histoire."))
        self.save()
    
    def remove_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)
            if quest not in self.quests_done:
                self.quests_done.append(quest)
            print(bold(f"La quête '{quest.get('name', None)}' a été complétée."))
        self.save()

    def get_level(self):
        return sum(map(lambda _: _["level"], self.get_quests_done()))

    def save(self):
        with open(PLAYER_FILE, 'w') as f:
            json.dump({
                'base_dir': self.base_dir,
                'level': self.get_level(),
                'quests': self.quests,
                'quests_done': self.quests_done,
                'commands': self.commands,
                'stories': self.stories
            }, f, indent=4)

    def load(self):
        try:
            with open(PLAYER_FILE, 'r') as f:
                data = json.load(f)
                self.base_dir = data.get('base_dir')
                self.level = data.get('level')
                self.quests = data.get('quests')
                self.quests_done = data.get('quests_done')
                self.commands = data.get('commands')
                self.stories = data.get('stories')
                return True
        except FileNotFoundError:
            return False

    def __repr__(self):
        return """Player:
Niveau={}

Quêtes en cours=
{}

Quêtes terminées=
{}

Commandes=
{}

Histoire=
{}
""".format(
        self.get_level(),
        '\n'.join([str(Quest(**q)) for q in self.quests]) if self.quests else 'Aucune',
        '\n'.join([str(Quest(**q)) for q in self.quests_done]) if self.quests_done else 'Aucune',
        '\n'.join([f'  - {x["name"]}: {x["desc"]}' for x in  self.commands]),
        '\n'.join([f'  - {x["desc"]}' for x in  [intro_story, *self.stories]])
    )

class NPC:
    def __init__(self, name, *args):
        self.name = name
        self.json_data = self.load_npc_data()

    def load_npc_data(self):
        npc_file = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(npc_file):
            raise FileNotFoundError(f"NPC file {npc_file} does not exist.")
        with open(npc_file, 'r') as f:
            return json.load(f)

    def get_name(self):
        return self.name

    def get_quests(self):
        return [quest for quest in self.json_data.get('quests', [])]

    def __repr__(self):
        return f"NPC(name={self.name})"

    def get_next_quest(self):
        quests = self.get_quests()
        if quests:
            return quests[0]
        return None

    def get_quest_validation_instance(self, quest_name):
        module_name, class_name = quest_name.rsplit('.', 1)
        try:
            module = importlib.import_module(module_name)
            quest_val_class = getattr(module, class_name)
            quest_val_instance = quest_val_class(self.get_next_quest(), Player(), os.path.join(os.getcwd(), self.name))
            return quest_val_instance
        except (ImportError, AttributeError) as e:
            print("DEBUG: ", e)
            return None 

    def check_quest(self, quest_name):
        quest_val_instance = self.get_quest_validation_instance(quest_name)
        if quest_val_instance:
            return quest_val_instance.validate_quest()
        return False, "Quest validation instance could not be created."

    def run_post_quest(self, quest_name):
        quest_val_instance = self.get_quest_validation_instance(quest_name)
        if quest_val_instance:
            quest_val_instance.post_quest()

    def check_done_quest_requirements(self, dep, player):
        requirements_met = 0
        for quest in player.get_quests_done():
            if quest.get('name') in dep:
               requirements_met += 1
        return requirements_met == len(dep)

    def check_doing_quest_requirements(self, dep, player):
        requirements_met = 0
        for quest in player.get_quests():
            if quest.get('name') in dep:
               requirements_met += 1
        return requirements_met == len(dep)

    def get_quest_setup_instance(self, setup_name):
        module_name, class_name = setup_name.rsplit('.', 1)
        try:
            module = importlib.import_module(module_name)
            setup_class = getattr(module, class_name)
            setup_instance = setup_class(Player(), os.path.join(os.getcwd(), self.name))
            return setup_instance
        except (ImportError, AttributeError) as e:
            print("DEBUG: ", e)
            return None


    def give_quest(self):
        quest_added = False
        player = Player()
        for npc_quest in self.get_quests():
            if npc_quest.get('name') not in [quest.get('name') for quest in player.get_all_quests()]:
                if self.check_done_quest_requirements(npc_quest.get('must_done', []), player) and \
                     self.check_doing_quest_requirements(npc_quest.get('must_doing', []), player):
                    quest_dialog = npc_quest.get('text', '')
                    npc_quest_setup = npc_quest.get('setup_script', None)
                    if npc_quest_setup:
                        setup_instance = self.get_quest_setup_instance(npc_quest_setup)
                        if setup_instance:
                            setup_instance.setup_quest()         
                    print(quest_dialog)
                    player.add_quest(npc_quest)
                    if npc_quest.get('level', 0) == 0:
                        self.talk(intro=False)  # Immediately validate and complete level 0 quests
                    else:
                        quest_added = True
                    break
        return quest_added
        

    def talk(self, intro=True):
        player = Player()
        talk = self.json_data.get('talk', '')
        # Print greeting message if it exists
        if talk and intro:
            print(bold(self.name) + ": " + talk)
        # Check and validate current quests 
        for player_quest in player.get_quests():
            if player_quest.get('name') in [quest.get('name') for quest in self.get_quests()]:
                quest_status, message = self.check_quest(player_quest.get('script'))
                # Print the message returned by the quest validation
                print(bold(self.name) + ": " + message)
                # If the quest is validated, run the post quest actions
                if quest_status:
                    self.run_post_quest(player_quest.get('script'))
                    player.remove_quest(player_quest)
                    player.add_reward(player_quest.get('rewards', []))
                else:
                    print(bold(self.name) + ": " + "La quête n'est pas encore terminée.")
        # Check for new quests to add
        if not self.give_quest():
            print(bold("Aucune autre quête disponible."))

ACTIONS = {
    'player': lambda _ : print(Player(*_)),
    'lnz': lambda _ : print(*(Zone().list_npcs()), sep='\n'),
    'talk': lambda _: NPC(*_).talk(),
}

if __name__ == "__main__":
    try:
        ACTIONS[os.path.basename(sys.argv[0])](sys.argv[1:])
    except Exception as e:
        print(bold(f"Impossible d'exécuter cette action."))
