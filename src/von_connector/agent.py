from .config import Configurator
from .helpers import uuid

from von_agent.nodepool import NodePool
from von_agent.agents import Issuer as VonIssuer
from von_agent.agents import Verifier as VonVerifier
from von_agent.agents import HolderProver as VonHolderProver

import logging
logger = logging.getLogger(__name__)

config = Configurator().config


class Issuer:
    def __init__(self):
        self.pool = NodePool(
            'permitify-issuer',
            '/app/.genesis')

        self.instance = VonIssuer(
            self.pool,
            config['wallet_seed'],
            config['name'] + ' Issuer Wallet',
            None,
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Verifier:
    def __init__(self):
        self.pool = NodePool(
            'permitify-verifier',
            '/app/.genesis')

        self.issuer = VonVerifier(
            self.pool,
            config['wallet_seed'],
            config['name'] + ' Verifier Wallet',
            None,
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Holder:
    def __init__(self):
        self.pool = NodePool(
            'permitify-holder',
            '/app/.genesis')

        self.issuer = VonHolderProver(
            self.pool,
            config['wallet_seed'],
            config['name'] + ' Holder Wallet',
            None,
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        await self.create_master_secret(uuid())
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()
