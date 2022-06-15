from random import randint
from typing import List

from enforce_typing import enforce_types

from ocean_lib.models.erc721_nft import ERC721NFT

INBOUND_KEY = "inbound_addrs"
OUTBOUND_KEY = "outbound_addrs"

@enforce_types
class NodeFactory:
    def __init__(self, ocean):
        self._ocean = ocean
    
    def newGoal(self, name:str, wallet):
        symbol = f"GOAL{randint(0,9999)}"
        return self._newNode(symbol, name, wallet)

    def newProject(self, name:str, wallet):
        symbol = f"PROJ{randint(0,9999)}"
        return self._newNode(symbol, name, wallet)

    def _newNode(self, symbol:str, name:str, wallet):
        data_nft = self._ocean.create_erc721_nft(symbol, name, wallet)
        node = Node()
        #https://stackoverflow.com/questions/60920784/python-how-to-convert-an-existing-parent-class-object-to-child-class-object
        node.__dict__.update(data_nft.__dict__)
        node.setData(INBOUND_KEY, " ", wallet)
        node.setData(OUTBOUND_KEY, " ", wallet)
        return node

@enforce_types
class Node(ERC721NFT):
    def __init__(self):
        pass

    #==== inbounds
    def getInboundNodes(self) -> List[str]:
        return self._getNodes(INBOUND_KEY)

    def getInboundAddrs(self) -> List[str]:
        return self._getAddrs(INBOUND_KEY)

    def addInboundNode(self, node, wallet):
        self.addInboundAddr(node.address, wallet)
        
    def addInboundAddr(self, node_address:str, wallet):
        self._addAddr(INBOUND_KEY, node_address, wallet)
        
    #==== outbounds
    def getOutboundNodes(self) -> List[str]:
        return self._getNodes(OUTBOUND_KEY)

    def getOutboundAddrs(self) -> List[str]:
        return self._getAddrs(OUTBOUND_KEY)

    def addOutboundNode(self, node, wallet):
        self.addOutboundAddr(node.address, wallet)

    def addOutboundAddr(self, node_address:str, wallet):
        self._addAddr(OUTBOUND_KEY, node_address, wallet)
        
    #==== helpers
    def _getNodes(self, key:str) -> List[str]:
        return [nodeAt(addr, self.web3) for addr in self._getAddrs(key)]
        
    def _getAddrs(self, key:str) -> List[str]:
        return self.getData(key).split()

    def _addAddr(self, key:str, address:str, wallet):
        s = self.getData(key)
        assert address not in s
        self.setData(key, f"{s} {address}", wallet) 

    def setData(self, key:str, value:str, wallet):
        # condition the key. ERC725 requires keccak256 hash
        key_hash = self.web3.keccak(text=key)  

        # condition the value. set_new_data() needs hex
        value_hex = value.encode('utf-8').hex()

        # actual work
        self.set_new_data(key_hash, value_hex, wallet)

    def getData(self, key:str) -> str:
        # condition the key
        key_hash = self.web3.keccak(text=key)

        # get the returned value
        value2_hex = self.get_data(key_hash)

        # condition the returned value
        value2 = value2_hex.decode('ascii')

        return value2

@enforce_types
def nodeAt(addr:str, web3) -> Node:
    """@return -- Goal or Project data nft, for the given address"""
    data_nft = ERC721NFT(web3, addr)
    return Node(data_nft)
