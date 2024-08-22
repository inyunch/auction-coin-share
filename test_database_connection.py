from sqlalchemy import create_engine

database_uri = 'sqlite:///auction/auction_dev.sqlite'
engine = create_engine(database_uri)

try:
    with engine.connect() as connection:
        print("Connection to the database was successful.")
except Exception as e:
    print(f"An error occurred: {e}")