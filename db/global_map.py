from models.game_state.FightItem import FightItem
from enums.sub_item_kind import SubItemKind
from enums.attacks.magic import Magic
from enums.item_kinds import ItemKind
import typing
import json

class MapDB:
    db: dict

    instance: 'MapDB'

    tart_map_areas: typing.List[dict]
    map_links: typing.List[dict]

    def __init__(self):
        self.db = json.loads(open('areaTpls.json', 'r', encoding='utf-8').read())
        self.links_db = json.loads(open('areaLinks.json', 'r', encoding='utf-8').read())

        self.tart_map_areas = []
        self.map_links = []

        self._load_items()
        self._load_links()

    def get_link_from(self, from_id: int):
        links = []
        for i in self.map_links:
            areaId = i.get('fromId', None)
            if (areaId and str(areaId) == str(from_id)):
                links.append((areaId, i.get('id')))

        return links

    def id_to_coords(self, cid: int,):
        area = self.db.get(str(cid), None)
        if (area):
            areaX = area.get('mapPosX', None)
            areaY = area.get('mapPosY', None)
            return (areaX, -areaY)
        
        return (None, None)
            

    def _load_links(self,):
        for i in self.links_db.values():
            self.map_links.append(i)

    def _load_items(self,):
        for i in self.db.values():
            map_id = i.get('mapId', 0)
            if (map_id == 52606): #tart
                self.tart_map_areas.append(i)

    @staticmethod
    def get_instance() -> 'MapDB':
        if (MapDB.instance is None):
            MapDB.instance = MapDB()
        
        return MapDB.instance

MapDB.instance = MapDB()