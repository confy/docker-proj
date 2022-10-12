import datetime
from xml.dom.pulldom import START_ELEMENT

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class Workout(Base):
    """Workout"""
    __tablename__ = 'workout'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_timestamp = Column(DateTime, nullable=False)
    end_timestamp = Column(DateTime, nullable=False)
    minimum_heart_rate = Column(Integer, nullable=False)
    peak_heart_rate = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)

    def __init__(self, start_timestamp, end_timestamp, minimum_heart_rate, peak_heart_rate, calories_burned):
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.minimum_heart_rate = minimum_heart_rate
        self.peak_heart_rate = peak_heart_rate
        self.calories_burned = calories_burned

    def to_dict(self):
        return {
            'id': self.id,
            'start_timestamp': self.start_timestamp,
            'end_timestamp': self.end_timestamp,
            'minimum_heart_rate': self.minimum_heart_rate,
            'peak_heart_rate': self.peak_heart_rate,
            'calories_burned': self.calories_burned
        }