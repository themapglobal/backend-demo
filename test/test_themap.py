import os
from enforce_typing import enforce_types

from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet

from .themap import NodeFactory, nodeAt

@enforce_types
def test1():
    # Create Ocean instance
    config = ExampleConfig.get_config()
    ocean = Ocean(config)

    # Create Alice's wallet
    private_key = os.getenv('TEST_PRIVATE_KEY1')
    wallet = Wallet(ocean.web3, private_key, config.block_confirmations, config.transaction_timeout)

    # Create a goal
    web3 = ocean.web3

    f = NodeFactory(ocean, wallet)

    goal_py_wasm = f.newGoal("Py run on WASM")
    goal_py_browser = f.newGoal("Py run in browser")

    goal_py_browser.addInbound(goal_py_wasm)

    proj_x = f.newProject("Proj: X", wallet)
    proj_x.addOutbound(goal_py_browser)

    proj_y = f.newProject("Proj: Y", wallet)
    proj_y.addOutbound(goal_py_browser)

    proj_pyscript = f.newProject("Project: Pyscript", wallet)
    proj_pyscript.addInbound(goal_py_wasm)
    proj_pyscript.addOutbound(goal_py_browser)
