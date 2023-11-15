from web3 import Web3
from server.config import settings
import json

web3 = Web3(Web3.HTTPProvider(settings.ethereum_url))
print(web3.is_connected())

bytecode = settings.byte_code
abi = json.load("abi.json")

address = settings.address
private_key = settings.private_key


def deploy_contract():
    nonce = web3.eth.get_transaction_count(address)
    gas_price = web3.to_wei('50', 'gwei')

    # Build the deployment transaction
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx = contract.constructor().build_transaction({
        'nonce': nonce,
        'gas': 4700000,
        'gasPrice': gas_price
    })

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(tx_hash)

    # Wait for the transaction to be mined
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(receipt)
    print(receipt["contractAddress"])

