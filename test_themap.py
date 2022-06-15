import os
from enforce_typing import enforce_types

from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet

from themap import NodeFactory, nodeAt

@enforce_types
def test1():
    # Create Ocean instance
    config = ExampleConfig.get_config()
    ocean = Ocean(config)

    # Create Alice's wallet
    private_key = os.getenv('TEST_PRIVATE_KEY1')
    wallet = Wallet(ocean.web3, private_key, config.block_confirmations, config.transaction_timeout)

    # Create goals
    f = NodeFactory(ocean)

    goal_py_wasm = f.newGoal("Py run on WASM", wallet)
    goal_py_browser = f.newGoal("Py run in browser", wallet)

    goal_py_browser.addInboundNode(goal_py_wasm, wallet)

    proj_x = f.newProject("Proj: X", wallet)
    proj_x.addOutboundNode(goal_py_browser, wallet)

    proj_y = f.newProject("Proj: Y", wallet)
    proj_y.addOutboundNode(goal_py_browser, wallet)

    proj_pyscript = f.newProject("Project: Pyscript", wallet)
    proj_pyscript.addInboundNode(goal_py_wasm, wallet)
    proj_pyscript.addOutboundNode(goal_py_browser, wallet)
