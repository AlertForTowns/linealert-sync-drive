# beadvol_writer.py

import os
from bead import Bead

class BeadVolumeWriter:
    def __init__(self, filepath):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def append_bead(self, bead: Bead):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(bead.to_json() + "\n")
