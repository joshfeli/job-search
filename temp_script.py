import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///job-search-results.db')

query = engine.execute('.tables;').fetchall()

print(query)