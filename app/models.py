from config import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Dish(db.Model):
    __tablename__ = 'dishes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    dining_hall_id = Column(Integer, ForeignKey('dining_halls.id'), nullable=False)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    
    # relationships
    dining_hall = relationship("DiningHall", back_populates="dishes")
    station = relationship("Station", back_populates="dishes")

    def __repr__(self):
        return f"<Dish(id={self.id}, name='{self.name}', category='{self.category}', dining_hall_name='{self.dining_hall.name}', station_name='{self.station.name}')>"

class DiningHall(db.Model):
    __tablename__ = 'dining_halls'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    
    # Relationship back to Dish and Station models
    dishes = relationship("Dish", back_populates="dining_hall")
    stations = relationship("Station", back_populates="dining_hall")

    def __repr__(self):
        return f"<DiningHall(id={self.id}, name='{self.name}')>"

class Station(db.Model):
    __tablename__ = 'stations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dining_hall_id = Column(Integer, ForeignKey('dining_halls.id'), nullable=False)
    
    # relationships
    dining_hall = relationship("DiningHall", back_populates="stations")
    dishes = relationship("Dish", back_populates="station")

    def __repr__(self):
        return f"<Station(id={self.id}, name='{self.name}', dining_hall_name='{self.dining_hall.name}')>"