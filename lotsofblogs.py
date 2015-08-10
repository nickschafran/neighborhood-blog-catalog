from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Region, Base, RegionBlog

engine = create_engine('sqlite:///regionblogs.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Manhattan
manhattan = Region(name="Manhattan")

session.add(manhattan)
session.commit()

boweryBoogie = RegionBlog(
    name="Bowery Boogie", description="test",
    url="http://www.boweryboogie.com/", region=manhattan)

session.add(boweryBoogie)
session.commit()

evGrieve = RegionBlog(
    name="EV Grieve", description="test",
    url="http://evgrieve.com/", region=manhattan)

session.add(evGrieve)
session.commit()

westSideRag = RegionBlog(
    name="West Side Rag", description="test",
    url="http://www.westsiderag.com/", region=manhattan)

session.add(westSideRag)
session.commit()

washSqBlog = RegionBlog(
    name="Washington Square Park Blog", description="test",
    url="http://www.washingtonsquareparkblog.com", region=manhattan)

session.add(washSqBlog)
session.commit()

tribecaCitizen = RegionBlog(
    name="Tribeca Citizen", description="test",
    url="http://tribecacitizen.com", region=manhattan)

session.add(tribecaCitizen)
session.commit()

morningsider = RegionBlog(
    name="Morningsider", description="test",
    url="http://morningsider.com", region=manhattan)

session.add(morningsider)
session.commit()

roosIslander = RegionBlog(
    name="Roosevelt Islander", description="test",
    url="http://rooseveltislander.blogspot.com", region=manhattan)

session.add(roosIslander)
session.commit()

# Brooklyn
brooklyn = Region(name="Brooklyn")

session.add(brooklyn)
session.commit()

bushwickDaily = RegionBlog(
    name="Bushwick Daily", description="test",
    url="http://bushwickdaily.com/", region=brooklyn)

session.add(bushwickDaily)
session.commit()

greenpointers = RegionBlog(
    name="Greenpointers", description="test",
    url="http://greenpointers.com/", region=brooklyn)

session.add(greenpointers)
session.commit()

freeWilliamsburg = RegionBlog(
    name="Free Williamsburg", description="test",
    url="http://freewilliamsburg.com/", region=brooklyn)

session.add(freeWilliamsburg)
session.commit()

brownstoner = RegionBlog(
    name="Brownstoner", description="test",
    url="http://www.brownstoner.com/", region=brooklyn)

session.add(brownstoner)
session.commit()

heresParkSlope = RegionBlog(
    name="Here's Park Slope", description="test",
    url="http://www.heresparkslope.com/", region=brooklyn)

session.add(heresParkSlope)
session.commit()

brokelyn = RegionBlog(
    name="Brokelyn", description="test",
    url="http://brokelyn.com/", region=brooklyn)

session.add(brokelyn)
session.commit()

ditmasParkCorner = RegionBlog(
    name="Ditmas Park Corner", description="test",
    url="http://ditmasparkcorner.com", region=brooklyn)

session.add(ditmasParkCorner)
session.commit()

SheepsheadBites = RegionBlog(
    name="Sheepshead Bites", description="test",
    url="http://www.sheepsheadbites.com", region=brooklyn)

session.add(SheepsheadBites)
session.commit()

BklynHeightsBlgo = RegionBlog(
    name="Brooklyn Heights Blog", description="test",
    url="http://brooklynheightsblog.com", region=brooklyn)

session.add(BklynHeightsBlgo)
session.commit()

rockawayist = RegionBlog(
    name="Rockawayist", description="test",
    url="http://rockawayist.com", region=brooklyn)

session.add(rockawayist)
session.commit()

# Queens
queens = Region(name="Queens")

session.add(queens)
session.commit()

queensCrap = RegionBlog(
    name="Queens Crap", description="test",
    url="http://queenscrap.blogspot.com/", region=queens)

session.add(queensCrap)
session.commit()

sunnysidePost = RegionBlog(
    name="Sunnyside Post", description="test",
    url="http://sunnysidepost.com/", region=queens)

session.add(sunnysidePost)
session.commit()

queensBrownstoner = RegionBlog(
    name="Brownstoner Queens", description="test",
    url="http://queens.brownstoner.com/", region=queens)

session.add(queensBrownstoner)
session.commit()

weHeartAstoria = RegionBlog(
    name="We Heart Astoria", description="test",
    url="http://weheartastoria.com/", region=queens)

session.add(weHeartAstoria)
session.commit()

licCourtSquare = RegionBlog(
    name="LIC Court Square", description="test",
    url="http://liccourtsquare.com", region=queens)

session.add(licCourtSquare)
session.commit()

# Bronx
bronx = Region(name="The Bronx")

session.add(bronx)
session.commit()

bronxSocialite = RegionBlog(
    name="Bronx Socialite", description="test",
    url="http://thebronxsocialite.com/", region=bronx)

session.add(bronxSocialite)
session.commit()

bronxCentric = RegionBlog(
    name="Bronx Centric", description="test",
    url="http://bronxcentric.org/", region=bronx)

session.add(bronxCentric)
session.commit()

bronxHipster = RegionBlog(
    name="Bronx Hipster", description="test",
    url="http://bronxhipster.tumblr.com/", region=bronx)

session.add(bronxHipster)
session.commit()

bronxMama = RegionBlog(
    name="Bronx Mama", description="test",
    url="http://bronxmama.com/", region=bronx)

session.add(bronxMama)
session.commit()

bronxPR = RegionBlog(
    name="Bronx PR", description="test",
    url="http://bronx-pr.com/", region=bronx)

session.add(bronxPR)
session.commit()

welcome2 = RegionBlog(
    name="Welcome 2 the Bronx", description="test",
    url="http://www.welcome2thebronx.com/wordpress/", region=bronx)

session.add(welcome2)
session.commit()

bronxBanter = RegionBlog(
    name="Bronx Banter", description="test",
    url="http://www.bronxbanterblog.com/", region=bronx)

session.add(bronxBanter)
session.commit()

# Staten Island
statenIsland = Region(name="Staten Island")

session.add(statenIsland)
session.commit()

statenIslandGenealogy = RegionBlog(
    name="Staten Island Genealogy", description="test",
    url="https://statenislandgenealogy.wordpress.com/", region=statenIsland)

session.add(statenIslandGenealogy)
session.commit()

# Hudson Valley
hudsonValley = Region(name="Hudson Valley")

session.add(hudsonValley)
session.commit()

newburghRest = RegionBlog(
    name="Newburgh Restoration", description="test",
    url="http://newburghrestoration.com/", region=hudsonValley)

session.add(newburghRest)
session.commit()

sloatsVill = RegionBlog(
    name="Sloatsburg Village", description="test",
    url="http://www.sloatsburgvillage.com", region=hudsonValley)

session.add(sloatsVill)
session.commit()

littleBeacon = RegionBlog(
    name="A Little Beacon Blog", description="test",
    url="http://www.alittlebeaconblog.com", region=hudsonValley)

session.add(littleBeacon)
session.commit()

goToHudson = RegionBlog(
    name="Go to Hudson", description="test",
    url="http://gotohudson.net/wordpress/", region=hudsonValley)

session.add(goToHudson)
session.commit()

haverstrawLife = RegionBlog(
    name="Haverstraw Life", description="test",
    url="http://haverstrawlife.com", region=hudsonValley)

session.add(haverstrawLife)
session.commit()

nyackFreeP = RegionBlog(
    name="Nyack Free Press", description="test",
    url="http://nyackfreepress.blogspot.com", region=hudsonValley)

session.add(nyackFreeP)
session.commit()

# Long Island
longIsland = Region(name="Long Island")

session.add(longIsland)
session.commit()

longIslandNewYork = RegionBlog(
    name="Long Island New York", description="test",
    url="http://longislandnewyork.blogspot.com", region=longIsland)

session.add(longIslandNewYork)
session.commit()

hamptonsChat = RegionBlog(
    name="Hamptons Chatter", description="test",
    url="http://hamptonschatter.blogspot.com", region=longIsland)

session.add(hamptonsChat)
session.commit()

# New Jersey
newJersey = Region(name="New Jersey")

session.add(newJersey)
session.commit()

hobGirl = RegionBlog(
    name="Hoboken Girl", description="test",
    url="http://hobokengirl.com", region=newJersey)

session.add(hobGirl)
session.commit()

chicPea = RegionBlog(
    name="Chic Pea Jersey City", description="test",
    url="http://www.chicpeajc.com", region=newJersey)

session.add(chicPea)
session.commit()

# Upstate
upstate = Region(name="Upstate New York")

session.add(upstate)
session.commit()

parlorCity = RegionBlog(
    name="Parlor City Punk", description="test",
    url="http://parlorcitypunk.tumblr.com", region=upstate)

session.add(parlorCity)
session.commit()

buffaloBlog = RegionBlog(
    name="Buffalo Blog", description="test",
    url="http://www.buffablog.com", region=upstate)

session.add(buffaloBlog)
session.commit()

buffaloRising = RegionBlog(
    name="Buffalo Rising", description="test",
    url="http://buffalorising.com", region=upstate)

session.add(buffaloRising)
session.commit()

northCountryRambler = RegionBlog(
    name="North Country Rambler", description="test",
    url="http://northcountryrambler.blogspot.com", region=upstate)

session.add(northCountryRambler)
session.commit()

rochesterSubway = RegionBlog(
    name="Rochester Subway", description="test",
    url="http://www.rochestersubway.com/", region=upstate)

session.add(rochesterSubway)
session.commit()

centralNY = RegionBlog(
    name="My Central New York", description="test",
    url="http://mycentralnewyork.blogspot.com", region=upstate)

session.add(centralNY)
session.commit()

print "added blogs!"
