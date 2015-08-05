import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Region(Base):
    """Regional categories to which blogs belong"""
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class RegionBlog(Base):
    """Blogs focusing on Regions"""
    __tablename__ = 'region_blog'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    url = Column(String(250))
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship(Region)

engine = create_engine('sqlite:///regionblogs.db')

Base.metadata.create_all(engine)
