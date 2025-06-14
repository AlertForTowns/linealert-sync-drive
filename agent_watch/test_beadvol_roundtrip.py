from beadcore.bead import Bead
from beadcore.beadvol_writer import BeadVolumeWriter
from beadcore.beadvol_reader import BeadVolumeReader
import time

# Write test
writer = BeadVolumeWriter("test.beadvol")
writer.append(Bead(time.time(), "setup_pkt", {"endpoint": 1}, label="init"))
writer.append(Bead(time.time(), "data_xfer", {"bytes": [0x12, 0x34]}, comment="test xfer"))
writer.close()

# Read back
reader = BeadVolumeReader("test.beadvol")
for bead in reader.stream_beads():
    print(bead.to_dict())
