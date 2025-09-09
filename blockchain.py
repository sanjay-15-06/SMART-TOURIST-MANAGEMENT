# File: blockchain.py
import hashlib
import json
from datetime import datetime

BLOCKCHAIN_FILE = "tourist_blockchain.json"

def load_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_blockchain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def create_block(digital_id, name, itinerary, emergency_contacts):
    block = {
        "digital_id": digital_id,
        "name": name,
        "itinerary": itinerary,
        "emergency_contacts": emergency_contacts,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    block["hash"] = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    return block

def add_block(digital_id, name, itinerary, emergency_contacts):
    chain = load_blockchain()
    block = create_block(digital_id, name, itinerary, emergency_contacts)
    chain.append(block)
    save_blockchain(chain)
    return block

def verify_id(digital_id):
    chain = load_blockchain()
    for block in chain:
        if block["digital_id"] == digital_id:
            return True, block
    return False, None

if __name__ == "__main__":
    blk = add_block("ID1001", "Test User", "Trip XYZ", "911")
    print("Blockchain Block Added:", blk)
    valid, data = verify_id("ID1001")
    print("Verification Result:", valid, data)
