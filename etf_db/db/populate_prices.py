import aiohttp
import asyncio
import asyncpg
import config
import datetime as dt
import json
import requests
import time


async def write_to_db(connection, params):
    await connection.copy_records_to_table('stock_price', records=params)
    # await connection.executemany("""
    #     INSERT INTO stock_price (stock_id, dt, open, high, low, close, volume)
    #     VALUES ($1, $2, $3, $4, $5, $6, $7)
    # """, params)


async def get_price(pool, stock_id, url):
    try:
        async with pool.acquire() as connection:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    resp = await response.read()
                    response = json.loads(resp)
                    params = [(stock_id, 
                               dt.datetime.fromtimestamp(bar['t']/1000),
                               bar['o'],
                               bar['h'],
                               bar['l'],
                               bar['c'],
                               bar['v'])]
                    await write_to_db(connection, params)
    except Exception as e:
        print(f'Unable to get URL {url}. Error: "{e.__class__}"')


async def get_prices(pool, symbol_urls):
    try:
        # Schedule aiohttp requests to run concurrently for all symbols
        ret = await asyncio.gather(*[get_price(pool, stock_id, symbol_urls[stock_id]) for stock_id in symbol_urls])
        print(f'Complete. Returned list of {len(ret)} prices')
    except Exception as e:
        print(e)


async def get_stocks():
    # Create database connection pool
    pool = await asyncpg.create_pool(user=config.DB_USER,
                                     password=config.DB_PASSWORD,
                                     database=config.DB_NAME,
                                     host=config.DB_HOST,
                                     command_timeout=None)
    # Get a connection
    async with pool.acquire() as connection:
        stocks = await connection.fetch("""
            SELECT *
            FROM stock
            WHERE id 
            IN (
                SELECT holding_id
                FROM etf_holding
            )
        """)
        symbol_urls = {}
        for stock in stocks:
            symbol_urls[stock['id']] = f"https://api.polygon.io/v2/aggs/ticker/{stock['symbol']}/range/5/minute/2020-10-01/2021-03-05?apiKey={config.API_KEY}&limit=50000"
    await get_prices(pool, symbol_urls)


start = time.time()
asyncio.run(get_stocks())
end = time.time()
print(f'Completed in {round(end - start, 3)} seconds')
