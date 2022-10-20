import asyncio

import aiofiles
from aiohttp import ClientSession
from eth_account import Account
from fake_useragent import FakeUserAgent as ua
from loguru import logger

import config

def get_headers(): return config.HEADERS.copy()

async def join_whitelist(worker: str) -> None:
    while True:
        account = Account.create("KEYSMASH FJAFJKLDSKF7JKFDJ 1530")
        public_key = account.address

        headers = get_headers()
        headers["User-Agent"] = ua().random

        async with ClientSession(headers=headers) as session:
            resp = await session.post(
                "https://ssrks0qeqf.execute-api.eu-west-2.amazonaws.com/production/whitelist/create",
                json={"wallet_address": public_key}
            )

        if resp.status == 200:
            logger.success(
                f"{worker} {public_key[:7]}... - successfully registered!")
        else:
            logger.error(f"{worker} - {public_key[:7]}... - {await resp.text()}")
            continue

        async with aiofiles.open("accounts.txt", "a+") as f:
            await f.write(f"{account.key.hex()}|{public_key}\n")
            
async def main():
    await asyncio.gather(
        *[
            asyncio.create_task(
                join_whitelist(
                    f"Worker {i+1}"
                )
            ) for i in range(config.THREADS)
        ]
    )