import alpaca_trade_api as tradeapi
import config
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # cursor_factory argument returns query results as a dictionary instead of a tuple
api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)

assets = api.list_assets()
for asset in assets:
    print(f'Inserting {asset.name} ({asset.symbol}) into stock table')
    cursor.execute("""
        INSERT INTO stock (name, symbol, exchange, is_etf)
        VALUES (%s, %s, %s, %s)
    """, (asset.name, asset.symbol, asset.exchange, False))

connection.commit()
