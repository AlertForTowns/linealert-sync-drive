# bead.py

import time
import json
import hashlib

class Bead:
    def __init__(self, payload, bead_type="log", tags=None, metadata=None):
        self.timestamp = time.time()
        self.payload = payload
        self.type = bead_type
        self.tags = tags or []
        self.metadata = metadata or {}
        self.id = self._generate_id()

    def _generate_id(self):
        return hashlib.sha256(f"{self.timestamp}{self.payload}".encode()).hexdigest()

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
            "tags": self.tags,
            "metadata": self.metadata,
            "payload": self.payload
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        bead = Bead(data["payload"], data["type"], data["tags"], data["metadata"])
        bead.timestamp = data["timestamp"]
        bead.id = data["id"]
        return bead
