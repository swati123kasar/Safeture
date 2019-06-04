import hashlib
import json
import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, render_template, jsonify, request


class Blockchain:
	#Initialize block chain
    def __init__(self):
        self.chain = []
        self.nodes = set()

        print ("Generating genesis block in Blockchain..")
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        print ("Registering new node..")
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

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """
        print ("Resolving conflicts called in Blockchain..")
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
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
            'location': 'Manufacturer',
            'timestamp': my_time,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'current_hash' : self.hash([len(self.chain)]),
            'medicine_id':'sanglipunecipla',
            'medicine':'cipla',
            'quantity': 30,
            'quality': 'GOOD',
        }

        self.chain.append(block)
        print ("current hash : "+block['current_hash'])
        #print ("Length of chain : "+str(len(self.chain)))

        return block
    """
    def new_transaction(self, sender, recipient, amount):
        
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
       
        print ("Starting new transaction in Blockchain class..")
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
    """

    def add_block(self,proof,previous_hash,request):
        print ("add_block called in Blockc	hain class..")
        print ("Length of chain : "+str(len(self.chain)))
        print ("previous hash : "+previous_hash)

        my_time=time.asctime(time.localtime(time.time()))

        block = {
            'index': len(self.chain) + 1,
            'timestamp': my_time,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'medicine_id':'sanglipunecipla',
            'medicine':'cipla',
            'quantity': 30,
            'location': str(request.remote_addr),
        }

        self.chain.append(block)
        #print ("Length of chain : "+strlen(self.chain))
        
        PARAMS={'address':"WCE, Sangli"}

        res = requests.post(url="http://127.0.0.1:80/get_data.php",params=PARAMS)
        print (res.url)

        return block

    @property
    def last_block(self):
        
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

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        #print ("proof of work....")

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        #print ("valid proof called....")

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route("/track_order",methods=['GET'])
def output():
        response = {
              'chain': blockchain.chain,
        }
        #c=json.dumps(response)
        
        chain=blockchain.chain
        return render_template("sample.php",chain_list=chain)

        if __name__ == "__main__":
	         app.run(host='10.60.1.243', port = '5000', debug = True)

@app.route('/add_block', methods=['GET'])
def add():
    print ("add_block() route called...")
    # We run the proof of work algorithm to get the next proof...
    #current_block = blockchain.current_block
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    
    """
    blockchain.new_transaction(
        sender="0",
        #recipient=node_identifier,
        recipient=str(request.remote_addr),
        amount=1,
    )
    """

    # Forge the new Block by adding it to the chain
    #current_hash = blockchain.hash(current_block)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.add_block(proof, previous_hash,request)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/get_data',methods=['GET'])
def respond():
    print (blockchain.chain)
    response=blockchain.chain
    """
    <table border=1>
    <tr backgroundcolor=green>
    <td>One of the best pop bands ever</td>
    </tr>
    </table>
    <table>
    """
    i=0
    for item in response.keys():
       print(i)
       i=i+1
       return "<table><tr><td>%s</td><td>%s</td></tr></table>" %(item,response[item])
    #"</table>"
    #return response

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        #'length': len(blockchain.chain),
    }
   
    #json_data=request.get_json()
    c=json.dumps(response)

    #print(c)
    return jsonify(response)


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
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
    app.run(host='10.60.1.243', port = '5000', debug = True)
