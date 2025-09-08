#!/bin/bash

ENGINE=$(basename -s .py $1)
echo "Please wait while setting up the environment..."
mkdir /tmp/bin
mkdir /tmp/bin/quests
cp quests/npc_def.py /tmp/bin/quests
cp $ENGINE.py /tmp/bin
for i in $(python3 -c "import $ENGINE; print(*$ENGINE.ACTIONS.keys())"); do
    bin=/tmp/bin/$i
    unlink $bin 2>/dev/null
    ln -s $ENGINE.py $bin
    chmod +x $bin
done

export PATH=/tmp/bin:$PATH



# Reset the map

python3 quests/npc_def.py > /dev/null 2>&1


# Set initial player state
cat > /tmp/player.json << EOF
{
    "name": "Player",
    "level": 0,
    "base_dir": "/tmp/game_map",
    "quests": [],
    "quests_done": [],
    "commands": [
        {"type": "command", "name": "talk", "desc": "Parler à un PNJ (ex: talk toto.npc)"},
        {"type": "command", "name": "player", "desc": "Afficher le statut du joueur"},
        {"type": "command", "name": "cd <directory>", "desc": "Changer de répertoire (changer de zone) (ex: cd village)"},
        {"type": "command", "name": "cd ..", "desc": "Remonter d'un répertoire (retourner à la zone précédente)"},
        {"type": "command", "name": "ls", "desc": "Lister les fichiers et répertoires (observer ce qui se trouve dans la zone) (ex: ls)"}          
    ],
    "stories": []
}
EOF

# Print initial message
cat << EOF
Welcome to the game!

=========================

You wake up in the middle of a road, with no memory of how you got there.
In fact you've lost almost all your memory.
The only thing you remember is:
- to walk: cd <somewhere>
- to walk back to the previous location: cd ..
- to look around: ls
- to talk: talk <npc>

EOF
