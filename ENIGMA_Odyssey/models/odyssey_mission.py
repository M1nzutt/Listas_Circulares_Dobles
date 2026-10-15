from dataclasses import dataclass, field
from typing import List
from models.odyssey_riddle import OdysseyRiddle


@dataclass
class OdysseyMission:
    id: str
    title: str
    description: str
    difficulty: str
    minutes: int
    puzzles: List[OdysseyRiddle] = field(default_factory=list)

    def validate(self) -> None:
        if not self.id.strip() or not self.title.strip():
            raise ValueError("La sala requiere ID y título.")
        if self.minutes < 1:
            raise ValueError("El tiempo debe ser de al menos un minuto.")
        ids = [p.id for p in self.puzzles]
        if len(ids) != len(set(ids)):
            raise ValueError("Los acertijos deben tener IDs únicos dentro de la sala.")
        for puzzle in self.puzzles:
            puzzle.validate()
