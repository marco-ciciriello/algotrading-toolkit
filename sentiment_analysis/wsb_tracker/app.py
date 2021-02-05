import config
import datetime as dt
import psycopg2
import psycopg2.extras

from psaw import PushshiftAPI

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # cursor_factory argument returns query results as a dictionary instead of a tuple

cursor.execute("""
    SELECT *
    FROM stock
""")

rows = cursor.fetchall()
stocks = ()
for row in rows:
    stocks['$' + row['symbol']] = row['id']

api = PushshiftAPI()

start_epoch = int(dt.datetime(2021, 2, 5).timestamp())

submissions = api.search_submissions(after=start_epoch,
                                     subreddit='wallstreetbets',
                                     filter=['url', 'author', 'title', 'subreddit'])

for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
    
    if len(cashtags) > 0:
        for cashtag in cashtags:
            submission_time = dt.datetime.fromtimestamp(submission.created_utc).isoformat()
            try:
                cursor.execute("""
                    INSERT INTO mention (stock_id, dt, message, source, url)
                    VALUES (%s, %s, %s, 'wallstreetbets', %s)
                """, (stocks[cashtag], submission_time, submission.title, submission.url))
                connection.commit()
            except Exception as e:
                print(e)
                connection.rollback()
