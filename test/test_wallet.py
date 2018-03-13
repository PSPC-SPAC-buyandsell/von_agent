"""
Copyright 2017-2018 Government of Canada - Public Services and Procurement Canada - buyandsell.gc.ca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from pathlib import Path

from von_agent.nodepool import NodePool
from von_agent.wallet import Wallet

import pytest


#noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_wallet(
    pool_name,
    pool_genesis_txn_path,
    pool_genesis_txn_file,
    path_home):

    pool = NodePool(pool_name, pool_genesis_txn_path, {'auto-remove': True})
    await pool.open()
    assert pool.handle is not None

    seed = '00000000000000000000000000000000'
    name = 'my-wallet'
    path = Path(path_home, 'wallet', name)

    async with Wallet(pool.name, seed, name, None, {'auto-remove': True}):
        pass
    assert not path.exists(), 'Wallet path still present at {}'.format(path)

    # 2. Default configuration (auto-remove=False)
    w = Wallet(pool.name, seed, name)

    await w.open()
    assert w.did
    assert w.verkey
    (did, verkey) = (w.did, w.verkey)
    await w.close()
    assert path.exists(), 'Wallet path removed at {}'.format(path)

    # 3. Make sure wallet opens from extant file
    x = Wallet(pool.name, seed, name, None, {'auto-remove': True})
    await x.open()
    assert did == x.did
    assert verkey == x.verkey

    await x.close()
    await pool.close()
    assert not path.exists(), 'Wallet path still present at {}'.format(path)
