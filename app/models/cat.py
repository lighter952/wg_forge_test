from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import ENUM
from .base import BaseModel


CatsColors = ENUM('black', 'white', 'black & white', 'red', 'red & white', 'red & black & white', name='cats_colors_enum')


class Cat(BaseModel):
    __tablename__ = 'cats'

    name = Column(VARCHAR(100), nullable=False)
    color = Column(CatsColors)
    tail_length = Column(Integer)
    whiskers_length = Column(Integer)
