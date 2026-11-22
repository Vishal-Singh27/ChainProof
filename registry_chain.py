import hashlib
import json
import time

class ModelBlock:
    def __init__(self, index, timestamp, model_id, model_name, version, model_hash, metrics, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.model_id = model_id
        self.model_name = model_name
        self.version = version
        self.model_hash = model_hash
        self.metrics = metrics
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "model_id": self.model_id,
            "model_name": self.model_name,
            "version": self.version,
            "model_hash": self.model_hash,
            "metrics": self.metrics,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

class ModelRegistryChain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = ModelBlock(
            index=0,
            timestamp=1700000000.0,
            model_id="GENESIS-ML-000",
            model_name="Genesis Governance Root",
            version="1.0.0",
            model_hash="0" * 64,
            metrics={"status": "Ledger initialized"},
            previous_hash="0" * 64,
            nonce=0
        )
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    def register_model(self, model_id, model_name, version, model_hash, metrics):
        new_block = ModelBlock(
            index=len(self.chain),
            timestamp=time.time(),
            model_id=model_id,
            model_name=model_name,
            version=version,
            model_hash=model_hash,
            metrics=metrics,
            previous_hash=self.last_block.hash
        )
        # PoW mining
        target = "0" * self.difficulty
        while not new_block.hash.startswith(target):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()

        self.chain.append(new_block)
        return new_block

    def verify_file_hash(self, file_hash):
        for b in self.chain:
            if b.model_hash == file_hash:
                return True, b
        return False, None
