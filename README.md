# The Map: Backend Demo

Use this README for a Python-based approach to populate a set of Goal and Project nodes, according to [The Map Software Spec](https://docs.google.com/document/d/1yS5EBGSbyfGnAQXkVqc-jKegME8xDbsephDIKAGOl0g/edit#heading=h.rjp9y39k12t7)

## 1. Setup
## Prerequisites

-   Linux/MacOS
-   [Docker](https://docs.docker.com/engine/install/), [Docker Compose](https://docs.docker.com/compose/install/), [allowing non-root users](https://www.thegeekdiary.com/run-docker-as-a-non-root-user/)
-   Python 3.8.5+

## Download barge and run services

Ocean `barge` runs ganache (local blockchain), Provider (data service), and Aquarius (metadata cache).

In a new console:

```console
# Grab repo
git clone https://github.com/oceanprotocol/barge
cd barge

# Clean up old containers (to be sure)
docker system prune -a --volumes

# Run barge: start Ganache, Provider, Aquarius; deploy contracts; update ~/.ocean
./start_ocean.sh
```

## Install the library from v4 sources

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

## 2. Publish Data NFTs for The Map

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
data_nft = ocean.create_data_nft('NFTToken1', 'NFT1', alice_wallet)
print(f"Created data NFT. Its address is {data_nft.address}")
```

FIXME: have >1 data NFTs, and fill in key-value pairs