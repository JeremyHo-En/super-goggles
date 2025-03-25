#%%
from web3 import Web3
from hexbytes import HexBytes
import json
import time

KEY = 'Key'
INFURA_URL = f"https://mainnet.infura.io/v3/{KEY}"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def classify_address(w3, address):
    try:
        address = Web3.to_checksum_address(address)

        # Check if it is an externally owned account (EOA)
        if not w3.eth.get_code(address):
            print('wallet')
            time.sleep(0.2)
            return 'wallet', address

        # Check if it is an ERC-20 token contract
        ERC20_ABI = '[{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
        contract = w3.eth.contract(address=address, abi=json.loads(ERC20_ABI))
        try:
            contract.functions.totalSupply().call()
            print("ERC-20")
            time.sleep(0.2)
            return 'ERC-20', address
        except:
            pass  

        # Check if it is an ERC-721 or ERC-1155 NFT contract
        ERC721_INTERFACE_ID = "0x80ac58cd"  # ERC-721
        ERC1155_INTERFACE_ID = "0xd9b67a26"  # ERC-1155
        try:
            if contract.functions.supportsInterface(ERC721_INTERFACE_ID).call():
                print("NFT (ERC-721)")
                return 'NFT', address
            if contract.functions.supportsInterface(ERC1155_INTERFACE_ID).call():
                print("NFT (ERC-1155)")
                return 'NFT', address
        except:
            pass  

        time.sleep(0.2)
        # Check if it is a Gnosis Safe (smart contract wallet)
        GNOSIS_ABI = '[{"constant":true,"inputs":[],"name":"getOwners","outputs":[{"name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"}]'
        contract = w3.eth.contract(address=address, abi=json.loads(GNOSIS_ABI))
        try:
            owners = contract.functions.getOwners().call()
            if owners:
                print("contract wallet")
                return 'wallet', address
        except:
            pass

        # Other smart contract
        print('Other contract')
        return 'Other', address

    except Exception as e:
        print(f'Error: {e}')
        return None

