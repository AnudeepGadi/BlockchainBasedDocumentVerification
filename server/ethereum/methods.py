from web3 import Web3
import json
from server.config import settings
from server.ethereum.sc_details import abi

web3 = Web3(Web3.HTTPProvider(settings.ethereum_url))

address = settings.address
private_key = settings.private_key


def add_record(encrypted_student_record):
    contract_address = settings.contract_address
    contract = web3.eth.contract(address=contract_address, abi=abi)
    transaction = contract.functions.addRecord(encrypted_student_record).build_transaction({
        "gas": 200000,  # Adjust gas limit as needed
        "gasPrice": web3.to_wei("50", "gwei"),  # Set a reasonable gas price
        "nonce": web3.eth.get_transaction_count(address),
    })
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    return receipt


def get_record(block_number: int):
    contract_address = settings.contract_address
    contract = web3.eth.contract(address=contract_address, abi=abi)
    record_data = contract.functions.getRecord().call(block_identifier=block_number)
    encrypted_text = record_data
    return encrypted_text

