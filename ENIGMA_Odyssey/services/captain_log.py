import json
import os
from pathlib import Path
from services.mission_archive import DATA_DIR


class CaptainLog:
    def __init__(self, path=None):
        self.path = Path(path) if path else DATA_DIR / 'progress.json'

    def load(self) -> dict:
        if not self.path.exists():
            return {}
        with self.path.open('r', encoding='utf-8') as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}

    def save(self, progress: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix('.tmp')
        try:
            with temp.open('w', encoding='utf-8') as handle:
                json.dump(progress, handle, ensure_ascii=False, indent=2)
            os.replace(temp, self.path)
        finally:
            if temp.exists():
                temp.unlink()
