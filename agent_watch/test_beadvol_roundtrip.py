# test_beadvol_roundtrip.py

import time
from beadcore.beadvol_writer import BeadVolumeWriter
from beadcore.beadvol_reader import BeadVolumeReader
from beadcore.bead import Bead

writer = BeadVolumeWriter("test_output.beadvol")
writer.append_bead(Bead(time.time(), "setup_pkt", {"endpoint": 1}, label="init"))
writer.append_bead(Bead(time.time(), "data_pkt", {"data": [0x01, 0x02]}, label="payload"))

print("Wrote 2 beads to test_output.beadvol")

print("Reading back contents...")
reader = BeadVolumeReader("test_output.beadvol")
for bead in reader:
    print(f"{bead.timestamp:.2f} | {bead.bead_type.upper():10} | {bead.payload} | {bead.label}")
