import hashlib
import json
from time import time


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_json(self):
        """
        Converts Transaction to JSON object

        :return: dict (JSON object)
        """
        return json.loads(json.dumps(self, default=lambda x: x.__dict__))

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a transaction

        :return: String hash
        """

        # Order dictionary to ensure consistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def sign(self, key):
        """
        
        """

    def is_valid(self):
        """

        """
