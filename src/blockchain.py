import hashlib
import requests
import json
from time import time
from urllib.parse import urlparse
from block import Block


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.add_to_chain(Block.genesis_block())

    def register_node(self, address):
        """
        Adds a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determines if a given blockchain is valid

        :param chain: Blockchain
        :return: True if valid
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            last_block_hash = Block.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Resolves conflicts by replacing local chain with the longest one in the network.

        :return: True if chain was replaced
        """

        neighbours = self.nodes
        new_chain = None

        # Only look for longer chains
        max_length = len(self.chain)

        # Grab and verify the chains from all nodes in network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer, and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace local chain if we discovered a new, valid, longer chain
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def add_to_chain(self, block):
        """
        Creates a new block in the blockchain

        :param block: The block to be added to the chain
        :return: New block
        """

        self.chain.append(block.to_json())

        # Reset the current list of transactions
        self.current_transactions = []

        return block.to_json()

    def create_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last block
        :return: <int> proof
        """

        last_proof = last_block['proof']
        last_hash = Block.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the proof

        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :param last_hash: <str> The hash of the previous block
        :return: <bool> True if valid.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
