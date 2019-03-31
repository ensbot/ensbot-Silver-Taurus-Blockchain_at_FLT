''' Node-Server on the network '''

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# ---------------------- Part-1: Building a Blockchain --------------------------------------------
class Blockchain:
    ''' Blockchain container class '''
    def __init__(self):
        self.chain =  []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
    
    def create_block(self, proof, previous_hash):
        ''' Method for creating a block '''
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
    
    @property
    def prev_block(self):
        ''' Getter for getting the previous block '''
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        ''' Method to get the proof of work '''
        new_proof = 1
        check = False
        while check is False:
            hash_op = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:4] == '0000':
                check = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        ''' Method to hash a block '''
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self, chain):
        ''' Method to check the chain is valid or not '''
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_op = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
   
    def add_transaction(self, sender, receiver, amount):
        ''' Method for adding different transactions in the Transaction field of the block '''
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        return self.prev_block['index'] + 1
    
    def add_node(self, address):
        ''' Method for adding a new node in the network '''
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        ''' Method for replacing the chain inside different nodes '''
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
      
          
# ---------------------- Part-2: Mining our Blockchain --------------------------------------------
# Creating a WebApp
app = Flask(__name__)

# Creating the address for the node on the Port - 5000 (Miner's address)
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    ''' Function for mining a block '''
    previous_block = blockchain.prev_block
    proof = blockchain.proof_of_work(previous_block['proof'])
    blockchain.add_transaction(sender = node_address, receiver = 'Kid', amount = 1)
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    response = {'message': 'Congratulations, you jsut mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    ''' Function to give a response on the basis of whether or not a chain is valid '''
    valid = blockchain.is_chain_valid()
    if valid:
        response = {'message': 'All good. The blockchain is valid!'}
    else:
        response = {'message': 'Silver, we have a problem. The Blockchain is not valid!'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_file = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json_file for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json_file['sender'], json_file['receiver'], json_file['amount'])
    response = {'message': f'This Transaction will be added to Block {index}'}
    return jsonify(response), 201


# ---------------------- Part-3: Decentralising our Blockchain ------------------------------------
# Connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    ''' Function to connect nodes in a network '''
    json_file = request.get_json()
    nodes = json_file.get('nodes')
    if nodes is None:
        return 'No Node', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are connected. The Silver Blockchain now contains the following node',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 200

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    ''' Function to give a response on the basis of whether or not a chain is replaced '''
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longer chain!',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 5002)
