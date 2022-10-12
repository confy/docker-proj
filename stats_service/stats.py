import pandas as pd

class Stats():
    def __init__(self, workouts: list) -> None:
        df = pd.DataFrame.from_records(
            [w.to_dict() for w in workouts]
        )
        duration_delta = df["end_timestamp"] - df["start_timestamp"]
        df["workout_duration_min"] = duration_delta.dt.total_seconds() / 60
        
        self.avg_peak_hr = df['peak_heart_rate'].mean()
        self.avg_min_hr = df['minimum_heart_rate'].mean()
        self.avg_cal_burned = df['calories_burned'].mean()
        self.avg_workout_duration = df["workout_duration_min"].mean()
        
        
    def to_dict(self):
        return {
            'avg_peak_hr': self.avg_peak_hr,
            'avg_min_hr': self.avg_min_hr,
            'avg_cal_burned': self.avg_cal_burned,
            'avg_workout_duration_minutes': self.avg_workout_duration
        }