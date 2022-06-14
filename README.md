# The Map: Backend Demo

This is a Python-based demo that populates some Goal and Project nodes

It follows **[The Map Spec](https://docs.google.com/document/d/1yS5EBGSbyfGnAQXkVqc-jKegME8xDbsephDIKAGOl0g/edit#heading=h.rjp9y39k12t7)**, and leverages Ocean data NFTs.

## 1. Setup
## Prerequisites

-   Linux/MacOS
-   [Docker](https://docs.docker.com/engine/install/), [Docker Compose](https://docs.docker.com/compose/install/), [allowing non-root users](https://www.thegeekdiary.com/run-docker-as-a-non-root-user/)
-   Python 3.8.5+

## Run local chain & Ocean services

Ocean `barge` runs Ganache (local blockchain), Provider (data service), and Aquarius (metadata cache).

In a new console:

```console
# Grab repo
git clone https://github.com/oceanprotocol/barge
cd barge

# Clean up old containers (to be sure)
docker system prune -a --volumes

# Start barge; deploy contracts; update ~/.ocean
./start_ocean.sh
```

## Install Ocean library

In a new console:

```console
# Create your working directory
mkdir my_project
cd my_project

# Initialize virtual environment and activate it. Install artifacts.
python3 -m venv venv
source venv/bin/activate

# Avoid errors for the step that follows
pip3 install wheel

# Install Ocean library. Allow pre-releases to get the latest v4 version.
pip3 install --pre ocean-lib
```

## Set envvars
```console
# Set envvars
export TEST_PRIVATE_KEY1=0x8467415bb2ba7c91084d932276214b11a3dd9bdb2930fefa194b666dd8020b99

# Set the address file only for ganache
export ADDRESS_FILE=~/.ocean/ocean-contracts/artifacts/address.json

# Set network URL
export OCEAN_NETWORK_URL=http://127.0.0.1:8545
```

## 2. Publish Data NFT

Open a new console and run python console with the command:
```console
python
```

In the Python console:

```python
# Create Ocean instance
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
config = ExampleConfig.get_config()
ocean = Ocean(config)

# Create Alice's wallet
import os
from ocean_lib.web3_internal.wallet import Wallet
alice_private_key = os.getenv('TEST_PRIVATE_KEY1')
alice_wallet = Wallet(ocean.web3, alice_private_key, config.block_confirmations, config.transaction_timeout)

# Publish a first data NFT
data_nft = ocean.create_data_nft('NFT1', 'NFT1', alice_wallet)
print(f"Created data NFT. Its address is {data_nft.address}")
```

## 3. Add key-value pair to data NFT

```python
# Key-value pair
key = "fav_color"
value = "blue"

# prep key for setter
key_hash = ocean.web3.keccak(text=key)  # Contract/ERC725 requires keccak256 hash

# prep value for setter
value_hex = value.encode('utf-8').hex()  # set_new_data() needs hex

# set
data_nft.set_new_data(key_hash, value_hex, alice_wallet)
```

## 4. Retrieve value from data NFT

```python
value2_hex = data_nft.get_data(key_hash)
value2 = value2_hex.decode('ascii')
print(f"Found that {key} = {value2}")
```

Under the hood, it uses [ERC725](https://erc725alliance.org/), which augments ERC721 with a well-defined way to set and get key-value pairs.