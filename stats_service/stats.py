import uuid
import pandas as pd
from datetime import datetime
from pydantic import Field

class Stats():
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    avg_peak_hr: float = Field(...)
    avg_min_hr: float = Field(...)
    avg_cal_burned: float = Field(...)
    avg_workout_duration: float = Field(...)
    date_calculated: datetime = Field(...)
    
    def __init__(self, workouts: list) -> None:
        df = pd.DataFrame.from_records(
            [w.to_dict() for w in workouts]
        )
        df['end_timestamp'] = pd.to_datetime(df['end_timestamp'], format='%Y-%m-%dT%H:%M:%S.%f%z')
        df['start_timestamp'] = pd.to_datetime(df['start_timestamp'], format='%Y-%m-%dT%H:%M:%S.%f%z')
        duration_delta = df["end_timestamp"] - df["start_timestamp"]
        df["workout_duration_min"] = duration_delta.dt.total_seconds() / 60
        
        self.avg_peak_hr = df['peak_heart_rate'].mean()
        self.avg_min_hr = df['minimum_heart_rate'].mean()
        self.avg_cal_burned = df['calories_burned'].mean()
        self.avg_workout_duration = df["workout_duration_min"].mean()
        self.date_calculated = datetime.utcnow()
        
        
    def to_dict(self):
        return {
            'avg_peak_hr': self.avg_peak_hr,
            'avg_min_hr': self.avg_min_hr,
            'avg_cal_burned': self.avg_cal_burned,
            'avg_workout_duration_minutes': self.avg_workout_duration,
            'date_calculated': self.date_calculated
        }