import time
from models.odyssey_mission import OdysseyMission
from models.odyssey_champion import OdysseyChampion
from structures.riddle_circuit import RiddleCircuit


class MissionDirector:
    def __init__(self, room: OdysseyMission, character: OdysseyChampion, saved=None, clock=None):
        self.room = room
        self.character = character
        self.chain = RiddleCircuit()
        for puzzle in room.puzzles:
            self.chain.append(puzzle)
        self.clock = clock or time.monotonic
        saved = saved or {}
        self.solved = {pid for pid in saved.get('solved', []) if pid in {p.id for p in room.puzzles}}
        self.hints_used = set(saved.get('hints_used', []))
        self.current = 0
        self.elapsed_before = max(0, int(saved.get('elapsed', 0)))
        self.started_at = self.clock()

    @property
    def elapsed(self) -> int:
        return self.elapsed_before + max(0, int(self.clock() - self.started_at))

    @property
    def expired(self) -> bool:
        return self.elapsed >= self.room.minutes * 60 and not self.completed

    @property
    def completed(self) -> bool:
        return len(self.chain) > 0 and all(p.id in self.solved for p in self.chain)

    @property
    def puzzle(self):
        return self.chain.get(self.current)

    def answer(self, text: str) -> bool:
        if self.expired or len(self.chain) == 0:
            return False
        correct = self.puzzle.matches(text)
        if correct:
            self.solved.add(self.puzzle.id)
        return correct

    def next(self) -> bool:
        if len(self.chain) == 0 or self.expired:
            return False
        if self.puzzle.id not in self.solved:
            return False
        new_index = self.chain.next_index(self.current)
        if new_index == 0 and not self.completed:
            return False
        self.current = new_index
        return True

    def previous(self) -> bool:
        if len(self.chain) == 0 or self.expired:
            return False
        new_index = self.chain.previous_index(self.current)
        if self.current == 0 and not self.completed:
            return False
        if self.chain.get(new_index).id not in self.solved:
            return False
        self.current = new_index
        return True

    def hint(self) -> str:
        self.hints_used.add(self.puzzle.id)
        return self.character.hint_prefix + self.puzzle.hint

    def snapshot(self) -> dict:
        return {'solved': sorted(self.solved), 'hints_used': sorted(self.hints_used), 'elapsed': self.elapsed}
