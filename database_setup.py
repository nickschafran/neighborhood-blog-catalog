#!/usr/bin/env python
"""Create regionblogs.db to serve the neighborhood blogs app."""
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Store user information."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Region(Base):
    """Regional categories to which blogs belong."""

    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    description = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description
        }


class RegionBlog(Base):
    """Blogs focusing on Regions."""

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
        """Return object data in easily serializeable format."""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'url': self.url,
        }


engine = create_engine('postgresql://catalog:password@localhost/catalog')

Base.metadata.create_all(engine)
