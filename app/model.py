from config import db
from sqlalchemy import Column, Integer, String, Text

class Dish(db.Model):
    __tablename__ = 'dishes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(255))
    dietary_info = Column(String(255))

    def __repr__(self):
        return f"<Dish(id={self.id}, name='{self.name}', category='{self.category}', dietary_info='{self.dietary_info}')>"