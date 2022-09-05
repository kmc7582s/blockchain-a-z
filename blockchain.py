# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
# 블록이 생성되고 정확한 날짜의 타임스탬프를 각 블록이 가지기 때문

import hashlib
# 블록을 해시할 때 사용

import json
# 블록을 해시하기 전에 블록 인코딩을 위해 이 라이브러리에서 dumps함수를 사용할 것이기 때문

from flask import Flask, jsonify
# Flask 라이브러리에서 Flask 클래스를 가져오고 웹 애플리케이션이 되는 Flask 클래스의 객체를 생성하기 때문
# Jsonify는 Postman에서 블록체인과 상호 작용할 때 메시지를 보내기 위해 사용하는 함수
# 예를 들어, Postman에서 전체 블록체인을 표시하기 위해 블록체인의 실제 상태를 요청할 때 사용할 수 있다.
# Jsonify를 사용해 요청에 관한 응답을 표시
# 새로운 블록을 채굴해 블록체인에 추가할 때도 마찬가지로 Jsonify를 사용해 Json 형식으로 채굴된 새로운 블록의 핵심 정보로 돌아간다.


# Part 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1, 
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        self.chain.append(block)
        return block

    
    def get_previous_block(self):
        return self.chain[-1]
        
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 + previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
        
    def hash(self, block):
        encodeed_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodeed_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 + previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
        
        
# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Congratulations, you just mined a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'All good. The Blockchain is valid'}
    else:
        response = {'message' : 'Houston, we have a problem. The Blockchain is not valid'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 8000)



