import config
import csv
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_HOST, 
                              database=config.DB_NAME, 
                              user=config.DB_USER, 
                              password=config.DB_PASSWORD)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""
    SELECT *
    FROM stock
    WHERE is_etf = True
""")

dates = ['2021-02-01']  # List of directories in which data is held
for current_date in dates:
    etfs = cursor.fetchall()
    for etf in etfs:
        with open(f'etf_db/data/{current_date}/{etf["symbol"]}.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ticker = row[3]
                if ticker:
                    shares = row[5]
                    weight = row[7]
                    cursor.execute("""
                        SELECT *
                        FROM stock
                        WHERE symbol = %s
                    """, (ticker,))
                    stock = cursor.fetchone()
                    if stock:
                        cursor.execute("""
                            INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (etf['id'], stock['id'], current_date, shares, weight))

connection.commit()
