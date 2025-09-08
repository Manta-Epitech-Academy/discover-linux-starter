#!/bin/ash

rm -fr /tmp/bin
rm -f /tmp/player.json 2>/dev/null
rm -rf /tmp/game_map

[[ -f /tmp/.installed ]] || (cd /home/user42/shell_rpg_engine; su user42 -c './install.sh engine.py; echo installed > /tmp/.installed')
