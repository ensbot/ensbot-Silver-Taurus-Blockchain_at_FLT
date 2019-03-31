''' Creating a simple and general Blockchain '''

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# ---------------------- Part-1: Building a Blockchain --------------------------------------------
class Blockchain:
    ''' Blockchain container class '''
    def __init__(self):
        self.chain =  []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        ''' Method for creating a block '''
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
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
    
# ---------------------- Part-2: Mining our Blockchain --------------------------------------------
# Creating a WebApp
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    ''' Function for mining a block '''
    previous_block = blockchain.prev_block
    proof = blockchain.proof_of_work(previous_block['proof'])
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    response = {'message': 'Congratulations, you jsut mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)
