import random
import time
from tqdm import tqdm
from web3 import Web3
from web3.eth import AsyncEth
from loguru import logger
import asyncio
from config import *
import pandas as pd

chains = {'bsc': ('https://rpc.ankr.com/bsc', 'https://bscscan.com/tx/'),
          'polygon': ('https://rpc.ankr.com/polygon', 'https://polygonscan.com/tx/'),
          'avax': ('https://rpc.ankr.com/avalanche', 'https://snowtrace.io/tx/')}

abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_owner","type":"address"},{"indexed":true,"internalType":"address","name":"_approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_owner","type":"address"},{"indexed":true,"internalType":"address","name":"_operator","type":"address"},{"indexed":false,"internalType":"bool","name":"_approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"source","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"FundsReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"_to","type":"address"},{"indexed":true,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"adminCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"purchase","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"fromChain","type":"uint32"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"bridgeIn","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"toChain","type":"uint32"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"bridgeOut","outputs":[{"internalType":"bytes4","name":"selector","type":"bytes4"},{"internalType":"bytes","name":"data","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burned","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"exists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAdmin","outputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"ownerAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"initPayload","type":"bytes"}],"name":"init","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_operator","type":"address"},{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"ownerCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"name":"setAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"ownerAddress","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"sourceBurn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sourceGetChainPrepend","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint224","name":"tokenId","type":"uint224"}],"name":"sourceMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"wallets","type":"address[]"},{"internalType":"uint224[]","name":"tokenIds","type":"uint224[]"}],"name":"sourceMintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint224[]","name":"tokenIds","type":"uint224[]"}],"name":"sourceMintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint224","name":"startingTokenId","type":"uint224"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"sourceMintBatchIncremental","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"sourceTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"tokens","outputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transfer","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'


class holograph:
    def __init__(self, privatekey, chain, mode):
        self.privatekey = privatekey
        self.chain = chain if chain else ''
        self.drop_address = Web3.to_checksum_address('0x8C531f965C05Fab8135d951e2aD0ad75CF3405A2')
        self.mode = mode
        self.count = random.randint(0,count_nfts)
    async def sleep_indicator(self,secs):
        for i in tqdm(range(secs), desc='жду', bar_format="{desc}: {n_fmt}c / {total_fmt}c {bar}", colour='green'):
            await asyncio.sleep(1)

    async def check_status_tx(self, tx_hash):
        w3 = Web3(Web3.AsyncHTTPProvider(chains[self.chain][0]), modules={'eth': (AsyncEth,)}, middlewares=[])
        account = w3.eth.account.from_key(self.privatekey)
        address = account.address

        logger.info(f'{address} - жду подтверждения транзакции')

        while True:
            try:
                status = await w3.eth.get_transaction_receipt(tx_hash)
                status = status['status']
                if status in [0, 1]:
                    return status
                time.sleep(1)
            except Exception as error:
                time.sleep(1)

    async def balance(self):
        chainss = ['avax', 'polygon', 'bsc']
        random.shuffle(chainss)

        for i in chainss:
            w3 = Web3(Web3.AsyncHTTPProvider(chains[i][0]), modules={'eth': (AsyncEth,)}, middlewares=[])
            acc = w3.eth.account.from_key(self.privatekey)
            address = acc.address
            balance = await w3.eth.get_balance(address)
            if balance > 0:
                return i

        return False
    async def mint(self):
        if self.mode == 1:
            chain = await self.balance()
            if chain:
                self.chain = chain
            else:
                return self.privatekey,'error'
        w3 = Web3(Web3.AsyncHTTPProvider(chains.get(self.chain)[0]), modules={'eth': (AsyncEth,)},
                  middlewares=[])
        acc = w3.eth.account.from_key(self.privatekey)
        address = acc.address
        while True:
            try:
                nonce = await w3.eth.get_transaction_count(address)
                contract = w3.eth.contract(address=self.drop_address, abi=abi)
                tx = await contract.functions.purchase(self.count).build_transaction({
                    'from': address,
                    'nonce': nonce,
                    'gas': await contract.functions.purchase(self.count).estimate_gas({'from': address, 'nonce': nonce}),
                    'gasPrice': await w3.eth.gas_price,
                })
                sign = acc.sign_transaction(tx)
                hash = await w3.eth.send_raw_transaction(sign.rawTransaction)
                status = await self.check_status_tx(hash)
                await self.sleep_indicator(5)
                if status == 1:
                    logger.info(f'{address}:{self.chain} - успешно заминтил {chains[self.chain][1]}{w3.to_hex(hash)}...')
                    return address,'success'
            except Exception as e:
                error = str(e)
                if "insufficient funds for gas * price + value" in error:
                    logger.error(f'{address}:{self.chain} - нет баланса нативного токена')
                elif 'nonce too low' in error or 'already known' in error:
                    logger.info(f'{address}:{self.chain} - успешно заминтил...')
                    return address,'success'
                else:
                    logger.error(f'{address}:{self.chain}  - {e}')
                    return address,'error'

async def main():
    tasks = []
    res = {'address': [],
           'result': []}

    with open("keys.txt", "r") as f:
        keys = [row.strip() for row in f]
        random.shuffle(keys)

    batches = [keys[i:i + 5] for i in range(0, len(keys), 5)]
    print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')
    for batch in batches:
        if mode == 0:
            for key in batch:
                chain = CHAIN
                boom = holograph(key, chain, mode)
                tasks.append(boom.mint())

        elif mode == 1:
            for key in batch:

                boom = holograph(key,mode=mode,chain=None)
                tasks.append(boom.mint())

        results = await asyncio.gather(*tasks)
        tasks = []

        for address, result in results:
            res['address'].append(address)
            res['result'].append(result)

    df = pd.DataFrame(res)
    df.to_csv('results.csv', mode='a', index=False)
    print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')
    print(f'\n{" " * 32}донат - 0xFD6594D11b13C6b1756E328cc13aC26742dBa868{" " * 32}\n')
    logger.info('mинетинг окончен...')


if __name__ == '__main__':
    asyncio.run(main())
