import tempfile
import unittest
from pathlib import Path
from controllers.mission_director import MissionDirector
from controllers.mission_architect import MissionArchitect
from models.odyssey_champion import CHARACTERS
from models.odyssey_riddle import OdysseyRiddle
from models.odyssey_mission import OdysseyMission
from services.mission_archive import MissionArchive
from services.captain_log import CaptainLog


class MissionPlayTests(unittest.TestCase):
    def setUp(self):
        self.room = OdysseyMission('demo', 'Sala', 'Demo', 'Fácil', 2, [
            OdysseyRiddle('1', 'Inicio', '', 'Capital de Colombia', 'Bogotá', 'Pista 1'),
            OdysseyRiddle('2', 'Final', '', '2+2', '4', 'Pista 2')])

    def test_lock_progress_and_circle(self):
        game = MissionDirector(self.room, CHARACTERS[0], clock=lambda: 0)
        self.assertFalse(game.next())
        self.assertFalse(game.previous())
        self.assertTrue(game.answer('bogota'))
        self.assertTrue(game.next())
        self.assertFalse(game.next())
        self.assertTrue(game.previous())
        self.assertTrue(game.next())
        self.assertTrue(game.answer('4'))
        self.assertTrue(game.completed)
        self.assertTrue(game.next())
        self.assertEqual(game.current, 0)
        self.assertTrue(game.previous())
        self.assertEqual(game.current, 1)

    def test_expiry(self):
        now = [0]
        game = MissionDirector(self.room, CHARACTERS[0], clock=lambda: now[0])
        now[0] = 121
        self.assertTrue(game.expired)
        self.assertFalse(game.answer('bogota'))

    def test_admin_and_persistence(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = MissionArchive(Path(temp) / 'rooms.json')
            MissionArchitect.insert(self.room, 1, OdysseyRiddle('3', 'Extra', '', '?', 'sí', '...'))
            self.assertEqual(self.room.puzzles[1].id, '3')
            MissionArchitect.delete(self.room, 1)
            self.assertEqual(len(self.room.puzzles), 2)
            repo.save([self.room])
            self.assertEqual(repo.load()[0].puzzles[0].id, '1')
            progress = CaptainLog(Path(temp) / 'progress.json')
            progress.save({'Yasuo:demo': {'elapsed': 9}})
            self.assertEqual(progress.load()['Yasuo:demo']['elapsed'], 9)


if __name__ == '__main__': unittest.main()
