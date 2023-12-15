import datetime

import db

class Habit:

    """Represents a habit

    Attributes:
        habit_name : str
            name of the habit
        description : str, optional
            description of the habit
        streak_value : Streak
            An instance of the Streak Class
        timespan : str
            frequency of the habit (daily/weekly)

    """
    def __init__(self, habit_name, timespan, description= None, streak_value= None):
        self.habit_name = habit_name
        self.description = description
        self.streak_value = Streak(habit_name)
        self.timespan = timespan

    def store(self,db):
        db.add_new_habit(db, self.habit_name, self.description, self.streak_value, self.timespan)


class Timespan:

    """Manages timespan for a habit

    Attribues
     habit_name : str
         Name of the habit.
     start_time : datetime
         Start time of the timespan.
     end_time : datetime
         End time of the timespan.

    """
    def __init__(self, habit_name, start_time= None, end_time= None):
        self.habit_name = habit_name
        self.start_time = start_time
        self.end_time = end_time

    def calc_timespan(self):
        self.start_time = db.get_start_time(self.habit_name)
        timespan = db.get_timespan_given_habit(self.habit_name)
        self.start_time = datetime.datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S.%f")
        if timespan == "weekly":
            self.end_time = self.start_time + datetime.timedelta(days=7)
            return self.end_time

        else:
            self.end_time = self.start_time + datetime.timedelta(days=1)
            return self.end_time


class Streak:

    """Manages Streak related logic

    Attributes
    habit_name : str
        Name of the habit.

    """
    def __init__(self, habit_name):
        self.habit_name = habit_name

    def update_streak(self, habit_name):
        streak = db.get_streak(habit_name)
        timespan_instance = Timespan(self.habit_name)
        end_time = timespan_instance.calc_timespan()

        if streak == 0:
            self.increment_streak(habit_name)
            streak_update = "Your streak has been incremented! Keep it up!"
            return streak_update
        else:
            now = datetime.datetime.now()
            if now < end_time:
                self.increment_streak(habit_name)
                streak_update = "Your streak has been incremented! Keep it up!"
                return streak_update
            else:
                self.reset_streak(habit_name)
                streak_update = "Sadly, you have failed to keep up this streak."
                return streak_update


    def increment_streak(self,habit_name):
        db.complete_habit(habit_name)


    def reset_streak(self, habit_name):
        db.reset_streak(habit_name)


