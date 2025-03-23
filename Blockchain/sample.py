import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def add_block(self, data):
        """Add a new block to the blockchain"""
        previous_block = self.chain[-1]
        new_block = self.create_block(previous_block, data)
        self.chain.append(new_block)

    def create_block(self, previous_block, data):
        """Create a new block"""
        index = previous_block.index + 1
        timestamp = time.time()
        hash = self.calculate_hash(index, previous_block.hash, timestamp, data)
        return Block(index, previous_block.hash, timestamp, data, hash)

    def calculate_hash(self, index, previous_hash, timestamp, data):
        """Calculate hash for a block"""
        block_string = f"{index}{previous_hash}{timestamp}{data}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def print_chain(self):
        """Print the blockchain"""
        for block in self.chain:
            print(f"Block {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print("-" * 40)


# Test the Blockchain
my_blockchain = Blockchain()

# Add blocks to the blockchain
my_blockchain.add_block("First block after genesis")
time.sleep(1)
my_blockchain.add_block("Second block after genesis")

# Print the blockchain
my_blockchain.print_chain()
