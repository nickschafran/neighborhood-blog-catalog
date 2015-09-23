#!/usr/bin/env python
#
# database_setup.py -- Creates regionblogs.db to serve the neighborhood blogs
# Flask application
#
# Author: Nick Schafran, Sept. 2015

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Stores user information"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Region(Base):
    """Regional categories to which blogs belong"""
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    description = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description
        }


class RegionBlog(Base):
    """Blogs focusing on Regions"""
    __tablename__ = 'region_blog'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    url = Column(String(250))
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship(Region)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'url': self.url,
        }


engine = create_engine('sqlite:///regionblogs.db')


Base.metadata.create_all(engine)
