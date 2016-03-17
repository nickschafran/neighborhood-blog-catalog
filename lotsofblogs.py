#!/usr/bin/env python
"""Populate db serving Neighborhood Blogs app with initial entries."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Region, Base, RegionBlog

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# User
User1 = User(
    name="Nick",
    email="nick@neighborhoods.com",
    picture='http://talksport.com/sites/default/files/field/image/201308/diego-maradona.jpg')
session.add(User1)
session.commit()

# Manhattan
manhattan = Region(
    user_id=1,
    name="Manhattan",
    description="New York County, a longer description will come")

session.add(manhattan)
session.commit()

boweryBoogie = RegionBlog(
    user_id=1,
    name="Bowery Boogie",
    description="Focuses on the area surrounding the Bowery",
    url="http://www.boweryboogie.com/", region=manhattan)

session.add(boweryBoogie)
session.commit()

evGrieve = RegionBlog(
    user_id=1,
    name="EV Grieve", description="Pessimisticly titled East Village blog",
    url="http://evgrieve.com/", region=manhattan)

session.add(evGrieve)
session.commit()

westSideRag = RegionBlog(
    user_id=1,
    name="West Side Rag", description="Covering the Upper West Side",
    url="http://www.westsiderag.com/", region=manhattan)

session.add(westSideRag)
session.commit()

washSqBlog = RegionBlog(
    user_id=1,
    name="Washington Square Park Blog",
    description="Greenwich Village based blog",
    url="http://www.washingtonsquareparkblog.com", region=manhattan)

session.add(washSqBlog)
session.commit()

tribecaCitizen = RegionBlog(
    user_id=1,
    name="Tribeca Citizen", description="Covering Tribeca",
    url="http://tribecacitizen.com", region=manhattan)

session.add(tribecaCitizen)
session.commit()

morningsider = RegionBlog(
    user_id=1,
    name="Morningsider", description="Covering the Morningside Heights area",
    url="http://morningsider.com", region=manhattan)

session.add(morningsider)
session.commit()

roosIslander = RegionBlog(
    user_id=1,
    name="Roosevelt Islander", description="Covering Roosevelt Island",
    url="http://rooseveltislander.blogspot.com", region=manhattan)

session.add(roosIslander)
session.commit()

# Brooklyn
brooklyn = Region(
    user_id=1,
    name="Brooklyn",
    description="Kings County, a longer description will come")

session.add(brooklyn)
session.commit()

bushwickDaily = RegionBlog(
    user_id=1,
    name="Bushwick Daily",
    description="Arts and development centered blog covering the Bushwick \
    and East Williamsburg Area",
    url="http://bushwickdaily.com/", region=brooklyn)

session.add(bushwickDaily)
session.commit()

greenpointers = RegionBlog(
    user_id=1,
    name="Greenpointers",
    description="Covering North Brooklyn, north of McCaren Park",
    url="http://greenpointers.com/", region=brooklyn)

session.add(greenpointers)
session.commit()

freeWilliamsburg = RegionBlog(
    user_id=1,
    name="Free Williamsburg", description="Longstanding Williamsburg blog",
    url="http://freewilliamsburg.com/", region=brooklyn)

session.add(freeWilliamsburg)
session.commit()

brownstoner = RegionBlog(
    user_id=1,
    name="Brownstoner", description="Development-focused Brooklyn blog",
    url="http://www.brownstoner.com/", region=brooklyn)

session.add(brownstoner)
session.commit()

heresParkSlope = RegionBlog(
    user_id=1,
    name="Here's Park Slope", description="Covering Park Slope",
    url="http://www.heresparkslope.com/", region=brooklyn)

session.add(heresParkSlope)
session.commit()

brokelyn = RegionBlog(
    user_id=1,
    name="Brokelyn",
    description="budget concious blog focusing on frugal events and meals \
    in Brooklyn",
    url="http://brokelyn.com/", region=brooklyn)

session.add(brokelyn)
session.commit()

ditmasParkCorner = RegionBlog(
    user_id=1,
    name="Ditmas Park Corner", description="Covering Ditmas Park",
    url="http://ditmasparkcorner.com", region=brooklyn)

session.add(ditmasParkCorner)
session.commit()

SheepsheadBites = RegionBlog(
    user_id=1,
    name="Sheepshead Bites", description="Food and drink in Sheepshead Bay",
    url="http://www.sheepsheadbites.com", region=brooklyn)

session.add(SheepsheadBites)
session.commit()

BklynHeightsBlgo = RegionBlog(
    user_id=1,
    name="Brooklyn Heights Blog", description="Covering Brooklyn Heights",
    url="http://brooklynheightsblog.com", region=brooklyn)

session.add(BklynHeightsBlgo)
session.commit()

rockawayist = RegionBlog(
    user_id=1,
    name="Rockawayist", description="Covering the Rockaways",
    url="http://rockawayist.com", region=brooklyn)

session.add(rockawayist)
session.commit()

# Queens
queens = Region(
    user_id=1,
    name="Queens", description="Queens County, a longer description will come")

session.add(queens)
session.commit()

queensCrap = RegionBlog(
    user_id=1,
    name="Queens Crap",
    description="blog dedicated to harshly criticizing the over-development of \
    Queens neighborhoods",
    url="http://queenscrap.blogspot.com/", region=queens)

session.add(queensCrap)
session.commit()

sunnysidePost = RegionBlog(
    user_id=1,
    name="Sunnyside Post", description="Covering Sunnyside",
    url="http://sunnysidepost.com/", region=queens)

session.add(sunnysidePost)
session.commit()

queensBrownstoner = RegionBlog(
    user_id=1,
    name="Brownstoner Queens",
    description="Queens offshoot of the development based blog",
    url="http://queens.brownstoner.com/", region=queens)

session.add(queensBrownstoner)
session.commit()

weHeartAstoria = RegionBlog(
    user_id=1,
    name="We Heart Astoria", description="Covering Astoria",
    url="http://weheartastoria.com/", region=queens)

session.add(weHeartAstoria)
session.commit()

licCourtSquare = RegionBlog(
    user_id=1,
    name="LIC Court Square", description="Covering Long Island City",
    url="http://liccourtsquare.com", region=queens)

session.add(licCourtSquare)
session.commit()

# Bronx
bronx = Region(
    user_id=1,
    name="The Bronx",
    description="bronx county, a longer description to come")

session.add(bronx)
session.commit()

bronxSocialite = RegionBlog(
    user_id=1,
    name="Bronx Socialite", description="Covering the Bronx",
    url="http://thebronxsocialite.com/", region=bronx)

session.add(bronxSocialite)
session.commit()

bronxCentric = RegionBlog(
    user_id=1,
    name="Bronx Centric", description="Covering the Bronx",
    url="http://bronxcentric.org/", region=bronx)

session.add(bronxCentric)
session.commit()

bronxHipster = RegionBlog(
    user_id=1,
    name="Bronx Hipster", description="Covering the Bronx",
    url="http://bronxhipster.tumblr.com/", region=bronx)

session.add(bronxHipster)
session.commit()

bronxMama = RegionBlog(
    user_id=1,
    name="Bronx Mama", description="Covering the Bronx",
    url="http://bronxmama.com/", region=bronx)

session.add(bronxMama)
session.commit()

bronxPR = RegionBlog(
    user_id=1,
    name="Bronx PR",
    description="Self proclaimed unnofficialBronx Public Relations site",
    url="http://bronx-pr.com/", region=bronx)

session.add(bronxPR)
session.commit()

welcome2 = RegionBlog(
    user_id=1,
    name="Welcome 2 the Bronx", description="Covering the Bronx",
    url="http://www.welcome2thebronx.com/wordpress/", region=bronx)

session.add(welcome2)
session.commit()

bronxBanter = RegionBlog(
    user_id=1,
    name="Bronx Banter", description="Covering the Bronx",
    url="http://www.bronxbanterblog.com/", region=bronx)

session.add(bronxBanter)
session.commit()

# Staten Island
statenIsland = Region(
    user_id=1,
    name="Staten Island",
    description="richmond county, a longer description to come")

session.add(statenIsland)
session.commit()

statenIslandGenealogy = RegionBlog(
    user_id=1,
    name="Staten Island Genealogy",
    description="Historically themed Staten Island blog",
    url="https://statenislandgenealogy.wordpress.com/", region=statenIsland)

session.add(statenIslandGenealogy)
session.commit()

# Hudson Valley
hudsonValley = Region(
    user_id=1,
    name="Hudson Valley",
    description="NY's hudson valley region")

session.add(hudsonValley)
session.commit()

newburghRest = RegionBlog(
    user_id=1,
    name="Newburgh Restoration",
    description="Covering the revitalization of historic Newburgh buildings",
    url="http://newburghrestoration.com/", region=hudsonValley)

session.add(newburghRest)
session.commit()

sloatsVill = RegionBlog(
    user_id=1,
    name="Sloatsburg Village",
    description="covering the Rockland and Orange County communities lining \
    Harriman State Park",
    url="http://www.sloatsburgvillage.com", region=hudsonValley)

session.add(sloatsVill)
session.commit()

littleBeacon = RegionBlog(
    user_id=1,
    name="A Little Beacon Blog", description="Covering Beacon, NY",
    url="http://www.alittlebeaconblog.com", region=hudsonValley)

session.add(littleBeacon)
session.commit()

goToHudson = RegionBlog(
    user_id=1,
    name="Go to Hudson", description="Covering Hudson, NY",
    url="http://gotohudson.net/wordpress/", region=hudsonValley)

session.add(goToHudson)
session.commit()

haverstrawLife = RegionBlog(
    user_id=1,
    name="Haverstraw Life", description="Covering Haverstraw, NY",
    url="http://haverstrawlife.com", region=hudsonValley)

session.add(haverstrawLife)
session.commit()

nyackFreeP = RegionBlog(
    user_id=1,
    name="Nyack Free Press", description="Covering Nyack, NY",
    url="http://nyackfreepress.blogspot.com", region=hudsonValley)

session.add(nyackFreeP)
session.commit()

# Long Island
longIsland = Region(
    user_id=1,
    name="Long Island",
    description="Nassau and Suffolk County NY")

session.add(longIsland)
session.commit()

longIslandNewYork = RegionBlog(
    user_id=1,
    name="Long Island New York", description="covering Long Island",
    url="http://longislandnewyork.blogspot.com", region=longIsland)

session.add(longIslandNewYork)
session.commit()

hamptonsChat = RegionBlog(
    user_id=1,
    name="Hamptons Chatter", description="covering the Hamptons",
    url="http://hamptonschatter.blogspot.com", region=longIsland)

session.add(hamptonsChat)
session.commit()

# New Jersey
newJersey = Region(
    user_id=1,
    name="New Jersey",
    description="The Garden State")

session.add(newJersey)
session.commit()

hobGirl = RegionBlog(
    user_id=1,
    name="Hoboken Girl", description="covering Hoboken, NJ",
    url="http://hobokengirl.com", region=newJersey)

session.add(hobGirl)
session.commit()

chicPea = RegionBlog(
    user_id=1,
    name="Chic Pea Jersey City", description="covering Jersey City, NJ",
    url="http://www.chicpeajc.com", region=newJersey)

session.add(chicPea)
session.commit()

# Upstate
upstate = Region(
    user_id=1,
    name="Upstate New York",
    description="Please don't take offense to the term Upstate")

session.add(upstate)
session.commit()

parlorCity = RegionBlog(
    user_id=1,
    name="Parlor City Punk",
    description="covering the Punk music scene in the Southern Tier",
    url="http://parlorcitypunk.tumblr.com", region=upstate)

session.add(parlorCity)
session.commit()

buffaloBlog = RegionBlog(
    user_id=1,
    name="Buffalo Blog", description="covering Buffalo, NY",
    url="http://www.buffablog.com", region=upstate)

session.add(buffaloBlog)
session.commit()

buffaloRising = RegionBlog(
    user_id=1,
    name="Buffalo Rising", description="covering Buffalo, NY",
    url="http://buffalorising.com", region=upstate)

session.add(buffaloRising)
session.commit()

northCountryRambler = RegionBlog(
    user_id=1,
    name="North Country Rambler",
    description="covering the North Country region in New York State",
    url="http://northcountryrambler.blogspot.com", region=upstate)

session.add(northCountryRambler)
session.commit()

rochesterSubway = RegionBlog(
    user_id=1,
    name="Rochester Subway", description="covering Rochester, NY",
    url="http://www.rochestersubway.com/", region=upstate)

session.add(rochesterSubway)
session.commit()

centralNY = RegionBlog(
    user_id=1,
    name="My Central New York", description="covering Central NY",
    url="http://mycentralnewyork.blogspot.com", region=upstate)

session.add(centralNY)
session.commit()

print "added blogs!"
