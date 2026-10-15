import json
import os
from pathlib import Path
from typing import List
from models.odyssey_riddle import OdysseyRiddle
from models.odyssey_mission import OdysseyMission

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get('ENIGMA_DATA_DIR', str(Path.home() / '.enigma_odyssey')))
SEED_PATH = BASE / 'data' / 'rooms_seed.json'


class MissionArchive:
    def __init__(self, path=None):
        self.path = Path(path) if path else DATA_DIR / 'rooms.json'

    def load(self) -> List[OdysseyMission]:
        source = self.path if self.path.exists() else SEED_PATH
        with source.open('r', encoding='utf-8') as handle:
            raw = json.load(handle)
        rooms = [OdysseyMission(id=r['id'], title=r['title'], description=r['description'], difficulty=r['difficulty'],
                      minutes=int(r['minutes']), puzzles=[OdysseyRiddle(**p) for p in r['puzzles']]) for r in raw]
        for room in rooms:
            room.validate()
        return rooms

    def save(self, rooms: List[OdysseyMission]) -> None:
        from dataclasses import asdict
        for room in rooms:
            room.validate()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix('.tmp')
        try:
            with tmp.open('w', encoding='utf-8') as handle:
                json.dump([asdict(room) for room in rooms], handle, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
        finally:
            if tmp.exists():
                tmp.unlink()
