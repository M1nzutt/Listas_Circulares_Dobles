import uuid
from models.odyssey_riddle import OdysseyRiddle
from models.odyssey_mission import OdysseyMission
from structures.riddle_circuit import RiddleCircuit


class MissionArchitect:
    @staticmethod
    def chain(room):
        chain = RiddleCircuit()
        for puzzle in room.puzzles:
            chain.append(puzzle)
        return chain

    @staticmethod
    def insert(room: OdysseyMission, index: int, puzzle: OdysseyRiddle) -> None:
        puzzle.validate()
        if any(p.id == puzzle.id for p in room.puzzles):
            raise ValueError('Ya existe un acertijo con ese ID.')
        chain = MissionArchitect.chain(room)
        chain.insert(index, puzzle)
        room.puzzles = list(chain)

    @staticmethod
    def delete(room: OdysseyMission, index: int) -> None:
        chain = MissionArchitect.chain(room)
        chain.remove_at(index)
        room.puzzles = list(chain)

    @staticmethod
    def update(room: OdysseyMission, index: int, puzzle: OdysseyRiddle) -> None:
        puzzle.validate()
        chain = MissionArchitect.chain(room)
        if any(p.id == puzzle.id for i, p in enumerate(chain) if i != index):
            raise ValueError('ID repetido.')
        chain.replace(index, puzzle)
        room.puzzles = list(chain)

    @staticmethod
    def make_puzzle(title, narrative, question, answer, hint, category):
        return OdysseyRiddle(id=str(uuid.uuid4())[:8], title=title.strip(), narrative=narrative.strip(),
                      question=question.strip(), answer=answer.strip(), hint=hint.strip(), category=category)
