from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Region, Base, RegionBlog

engine = create_engine('sqlite:///regionblogs.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Manhattan
manhattan = Region(name="Manhattan")

session.add(manhattan)
session.commit()

# Brooklyn
brooklyn = Region(name="Brooklyn")

session.add(brooklyn)
session.commit()

# Queens
queens = Region(name="Queens")

session.add(queens)
session.commit()

# Bronx
bronx = Region(name="The Bronx")

session.add(bronx)
session.commit()

# Staten Island
statenIsland = Region(name="Staten Island")

session.add(statenIsland)
session.commit()

# Hudson Valley
hudsonValley = Region(name="Hudson Valley")

session.add(hudsonValley)
session.commit()

# Long Island
longIsland = Region(name="Long Island")

session.add(longIsland)
session.commit()

# New Jersey
newJersey = Region(name="New Jersey")

session.add(newJersey)
session.commit()

# Upstate
upstate = Region(name="Upstate New York")

session.add(upstate)
session.commit()

print "added blogs!"
