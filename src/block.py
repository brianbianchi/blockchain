import hashlib
import json
from time import time


class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def to_json(self):
        """
        Converts Block to JSON object

        :return: dict (JSON object)
        """
        return json.loads(json.dumps(self, default=lambda x: x.__dict__))

    @staticmethod
    def genesis_block():
        """
        Defines genesis block

        :return: Block
        """
        return Block(0, time(), [], 100, '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b')

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :return: String hash
        """

        # Order dictionary to ensure consistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
