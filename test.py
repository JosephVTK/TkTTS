import unittest
import os

from uuid import uuid4
from pathlib import Path

from tktts import MainWindow, gtts

class TestWindow(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()
        self.keys = gtts.lang.tts_langs().keys()

    def test_count_elements(self):
        self.assertEqual(9, len(self.window.elements.keys()))

    def test_combo_keys(self):
        self.assertGreaterEqual(len(self.keys), 10)
        self.assertEqual(list(self.keys), list(self.window.elements["comboLanguage"]['values']))

    def test_unique_filename(self):
        uuid_str = str(uuid4())
        Path(f'{uuid_str}.mp3').touch()

        new_string = self.window._get_unique_filename(uuid_str)
        self.assertEqual(new_string, uuid_str + ' (1).mp3')
        os.remove(f'{uuid_str}.mp3')

if __name__ == '__main__':
    unittest.main()