from translation_tab import *
from config import T


base = "/tmp/game_map"

village_path = f"{base}/{village[T]}"
montagne_path = f"{base}/{mountain[T]}"
foret_path = f"{base}/{forest[T]}"
mer_for_path = f"{foret_path}/{sea[T]}"
tunnel_path = f"{montagne_path}/{tunnel[T]}"
route_de_montagne_path = f"{tunnel_path}/{mountain_road[T]}"
vallee_path = f"{route_de_montagne_path}/{valley[T]}"
lac_path = f"{route_de_montagne_path}/{lake[T]}"
mer_lac_path = f"{lac_path}/{sea[T]}"
fond_du_lac_path = f"{lac_path}/{lake_bottom[T]}"
passage_secret_path = f"{montagne_path}/{secret_passage[T]}"
chateau_path = f"{vallee_path}/{castle[T]}"
bibliotheque_path = f"{chateau_path}/{library[T]}"
salle_du_trone_path = f"{chateau_path}/{throne_room[T]}"
donjon_path = f"{chateau_path}/{dungeon[T]}"