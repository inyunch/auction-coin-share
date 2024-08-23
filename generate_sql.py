from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from auction.models import db, User, Group, Listing, Review, WatchListItem, Bid

# Create an in-memory SQLite database
# engine = create_engine('sqlite:///:auction_dev:')
engine = create_engine('sqlite:///auction_dev.sqlite')


# Bind the engine to the metadata of the Base class so that
# the declaratives can be accessed through a DBSession instance
db.metadata.create_all(engine)

# Print the SQL statements
for table in db.metadata.sorted_tables:
    print(CreateTable(table).compile(engine))