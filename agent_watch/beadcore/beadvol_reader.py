# beadvol_reader.py

from bead import Bead

class BeadVolumeReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_beads(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                yield Bead.from_json(line.strip())
