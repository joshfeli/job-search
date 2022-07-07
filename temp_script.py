import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///job-search-results.db')

query = engine.execute('SELECT COUNT(user_id) FROM jobs WHERE user_id="joshua_feliciano"').fetchone()

print(query[0])