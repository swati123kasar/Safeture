import hashlib
import json
import time
import serial
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain:
    #Initialize block chain
    
    def __init__(self):
        self.chain = []
        self.nodes = set()

        print ("Generating genesis block in Blockchain..")
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """
        print ("Validating the chain in blockchain..")
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        
        print ("Resolving conflicts called in Blockchain..")
        neighbours = self.nodes
        new_chain = None

        
        max_length = len(self.chain)

        
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        print ("Adding new block in Blockchain..")
        print ("Length of chain : "+str(len(self.chain)))

        my_time=time.asctime(time.localtime(time.time()))

        block = {
            'index': len(self.chain) + 1,
            'timestamp': my_time,
            #'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            #'current_hash' : self.hash([len(self.chain)]),
            'medicine_id':'sanglipunecipla',
            'medicine':'cipla',
            'quantity': 30,
            'quality': 'GOOD',
        }

        self.chain.append(block)
        #print ("current hash : "+block['current_hash'])
        print ("Length of chain : "+str(len(self.chain)))

        return block
    

    def add_block(self,previous_hash,request):
        print ("add_block called in Blockchain class..")
        print ("Length of chain : "+str(len(self.chain)))
        #print ("current hash : "+current_hash)
        print ("previous hash : "+previous_hash)

        my_time=time.asctime(time.localtime(time.time()))

        condition=self.sense_data()

        block = {
            'index': len(self.chain) + 1,
            'timestamp': my_time,
            #'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            #'current_hash': current_hash or self.hash(len(self.chain)),
            'medicine_id':'sanglipunecipla',
            'medicine':'cipla',
            'quantity': 30,
            'location': str(request.remote_addr),
            'quality':condition,
        }

        self.chain.append(block)
        print ("Length of chain : "+str(len(self.chain)))
        return block

    @staticmethod
    def sense_data():
        ser=serial.Serial('COM4',9600)
        arr=[]
        arr1=[]
        x=0

        while x<5:
              t=ser.readline()
              z=int(t)
              if z<=40 and z>=20:
                arr.append(z)
              x+=1

        print(arr)
        for i in arr:
            if i<=30 and i>=25:
               arr1.append("yes")
            else:
               arr1.append("no")

        for j in arr1:
            if j=="no":
               return 'BAD'
               break
            else:
               return 'GOOD'
               break

    @property
    def last_block(self):
        #print (self.chain[-1]['current_hash'])
        return self.chain[-1]
    """
    @property
    def current_block(self):
        return self.chain[0]
    """
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def task(self, last_block):
        

        

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/add_block', methods=['GET'])
def add():
    print ("add_block() route called...")
    
    #current_block = blockchain.current_block
    last_block = blockchain.last_block
    #proof = blockchain.task(last_block)

    

    # Forge the new Block by adding it to the chain
    #current_hash = blockchain.hash(current_block)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.add_block(previous_hash,request)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        #'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/get_data',methods=['GET'])
def respond():
    print (blockchain.chain)
    response=json.dumps(blockchain.chain)
    return response


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


# Example
data = {}
data['key'] =blockchain.chain

writeToJSONFile('./','test1',data)



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200





@app.route('/nodes/resolve', methods=['GET'])
def check():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    """from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port"""

    # app.run(debug = True)
    #app.run(host='192.168.43.194', port = '5000', debug = True)
    app.run(host='10.60.1.103', port = '5000', debug = True)
    #app.run(debug = True)