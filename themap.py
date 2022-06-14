from random import randint
from ocean_lib.models.ERC721NFT import ERC721NFT

INBOUND_KEY = "inbound_addrs"
OUTBOUND_KEY = "outbound_addrs"

def nodeAt(addr:str, web3) -> Node:
    """@return -- Goal or Project data nft, for the given address"""
    data_nft = ERC721NFT(self._ocean.web3, addr)
    return Node(data_nft)

class NodeFactory:
    def __init__(self, ocean, wallet):
        self._ocean = ocean
        self._wallet = wallet
    
    def newGoal(self, name:str):
        symbol = f"GOAL{randint(0,9999)}"
        return self._newNode(symbol, name)

    def newProject(name:str):
        symbol = f"PROJ{randint(0,9999)}"
        return self._newNode(symbol, name, ocean, wallet)

    def _newNode(symbol:str, name:str):
        data_nft = self._ocean.create_erc721_nft(symbol, name, self._wallet)
        return Node(data_nft, self._ocean)

class Node:
    def __init__(self, data_nft, ocean):
        self._ocean = ocean
        self._setData(INBOUND_KEY, " ")
        self._setData(OUTBOUND_KEY, " ") # typically just Projects

    #==== inbounds
    def getInboundNodes(self) -> List[str]:
        return self._getNodes(INBOUND_KEY)

    def getInboundAddrs(self) -> List[str]:
        return self._getAddrs(INBOUND_KEY)

    def addInboundNode(self, node, wallet):
        self.addInboundAddr(node.address, wallet)
        
    def addInboundAddr(self, node_address:str, wallet):
        self._addAddr(INBOUND_KEY, node_address)
        
    #==== outbounds
    def getOutboundNodes(self) -> List[str]:
        return self._getNodes(OUTBOUND_KEY)

    def getOutboundAddrs(self) -> List[str]:
        return self._getAddrs(OUTBOUND_KEY)

    def addOutboundNode(self, node, wallet):
        self.addOutboundAddr(node.address, wallet)

    def addOutboundAddr(self, node_address:str, wallet):
        self._addAddr(OUTBOUND_KEY)
        
    #==== helpers
    def _getNodes(self, key:str) -> List[str]:
        return [nodeAt(addr, self._ocean.web3) for addr in self._getAddrs(key)]
        
    def _getAddrs(self, key:str) -> List[str]:
        return self._getData(key).split()

    def addAddr(self, key:str, address:str, wallet):
        s = self._getData(key)
        assert address not in s
        self._setData(key, f"{s} {address}", wallet) 

    def _setData(self, key:str, value:str, wallet):
        # condition the key. ERC725 requires keccak256 hash
        key_hash = self._ocean.web3.keccak(text=key)  

        # condition the value. set_new_data() needs hex
        value_hex = value.encode('utf-8').hex()

        # actual work
        self.data_nft.set_new_data(key_hash, value_hex, wallet)

    def _getData(self, key:str) -> str:
        # condition the key
        key_hash = self._ocean.web3.keccak(text=key)

        # get the returned value
        value2_hex = self.data_nft.get_data(key_hash)

        # condition the returned value
        value2 = value2_hex.decode('ascii')

        return value2
