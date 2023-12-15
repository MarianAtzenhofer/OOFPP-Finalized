import sqlite3
import datetime




def create_tables(db):
    """create a Habit table as well as a Streak table if they don't exist already"""

    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Habit (
                Habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Habit_name TEXT NOT NULL,
                timespan TEXT NOT NULL,
                description TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Streak (
               Habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
               Habit_name TEXT,
               Date TEXT,
               start_time INTEGER,
               completed_boolean INTEGER NOT NULL CHECK (completed_boolean IN (0, 1)),
               Streak INTEGER NOT NULL,
               longest_Streak INTEGER NOT NULL, 
               FOREIGN KEY(Habit_id) REFERENCES Habit(Habit_id))""")

    db.commit()


def get_db(name="db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


db = get_db()

def get_streak(habit_name):
    cur = db.cursor()
    streak = cur.execute("SELECT Streak From Streak WHERE Habit_name = ?", (habit_name,)).fetchone()
    db.commit()
    return int(streak[0])


def get_all_tracked_habits():
    cur = db.cursor()
    all_tracked_habits = cur.execute("SELECT Habit_name FROM Habit").fetchall()
    db.commit()
    return all_tracked_habits


def get_start_time(habit_name):
    cur = db.cursor()
    start_time_tuple = cur.execute("SELECT start_time FROM Streak WHERE Habit_name = ?", (habit_name,)).fetchone()
    start_time = start_time_tuple[0]
    db.commit()
    return start_time


def get_streak_given_habit(habit_name):
    cur = db.cursor()
    query = cur.execute("SELECT Streak FROM Streak WHERE Habit_name = ?", (habit_name,)).fetchone()
    streak = query[0]
    db.commit()
    return int(streak)


def complete_habit(habit_name, date=None):
    cur = db.cursor()
    start_time = get_start_time(habit_name)
    # save time at which the streak has been updated
    cur.execute("UPDATE Streak "
                "SET start_time = ?"
                "WHERE Habit_name = ?",
                (start_time, habit_name,))

    # change boolean to 1 so habit is saved as done
    cur.execute("UPDATE Streak "
                "SET completed_boolean = ?"
                "WHERE Habit_name = ?",
                (1, habit_name,))

    # increment streak value in streak table
    cur.execute("UPDATE Streak "
                "SET streak = streak + 1 "
                "WHERE Habit_name = ?",
                (habit_name,))

    # increment longest_streak if possible
    streak = get_streak_given_habit(habit_name)
    longest_streak = cur.execute("SELECT longest_streak FROM Streak WHERE Habit_name = ?", (habit_name,)).fetchone()

    if streak > longest_streak[0]:
        cur.execute("UPDATE Streak "
                    "SET longest_streak = ? "
                    "WHERE Habit_name = ?",
                    (streak, habit_name))
    else:
        pass
    db.commit()


def get_boolean_value(habit_name):
    cur = db.cursor()
    boolean_value = cur.execute("SELECT boolean_value WHERE Habit_name = ?", (habit_name,)).fetchone()
    db.commit()
    return boolean_value


def get_unchecked_habits():
    cur = db.cursor()
    unchecked_habits = cur.execute("SELECT Habit_name FROM Streak WHERE Completed_Boolean = ?", (0,)).fetchall()
    db.commit()
    return unchecked_habits


def add_new_habit(habit_name, timespan, description, streak_value=0):
    # adds data for a new habit in both Habit and Streak table
    cur = db.cursor()
    start_time = datetime.datetime.now()
    cur.execute("INSERT INTO Habit "
                "(Habit_name , timespan, description) "
                "VALUES(?, ?, ?)",
                (str(habit_name), str(timespan), str(description)))
    cur.execute("INSERT INTO Streak "
                "(Habit_name, start_time, completed_boolean, Streak, longest_Streak) "
                "VALUES (?, ?, ?, ?, ?)",
                (str(habit_name), start_time, 0, streak_value, 0))
    db.commit()


def reset_streak(habit_name):
    cur = db.cursor()
    start_time = get_start_time(habit_name)
    # save time at which the streak has been updated
    cur.execute("UPDATE Streak "
                "SET start_time = ?"
                "WHERE Habit_name = ?",
                (start_time, habit_name,))

    # change boolean to 0 so habit is saved as not done yet
    cur.execute("UPDATE Streak "
                "SET completed_boolean = ?"
                "WHERE Habit_name = ?",
                (0, habit_name,))

    # update streak value in streak table
    cur.execute("UPDATE Streak "
                "SET streak = ? "
                "WHERE Habit_name = ?",
                (0, habit_name,))
    db.commit()


def del_habit(habit_name):
    cur = db.cursor()
    cur.execute("DELETE FROM Habit WHERE Habit_name = ?", (habit_name,))
    cur.execute("DELETE FROM Streak WHERE Habit_name =?", (habit_name,))
    db.commit()


def get_timespan_given_habit(habit_name):
    cur = db.cursor()
    timespan_given_habit = cur.execute("SELECT timespan FROM Habit WHERE Habit_name = ?", (habit_name,)).fetchone()
    db.commit()
    return list(timespan_given_habit)


def get_highest_streak():
    cur = db.cursor()
    highest_streak = cur.execute("SELECT MAX(Streak) FROM Streak").fetchone()
    db.commit()
    return int(highest_streak[0])


def get_all_habits_same_periodicity(timespan):
    cur = db.cursor()
    habits_same_periodicity = cur.execute("SELECT * FROM Habit WHERE timespan = ?", (timespan,)).fetchall()
    db.commit()
    return list(habits_same_periodicity)


def get_longest_streak_given_habit(habit_name):
    cur = db.cursor()
    longest_streak = cur.execute("SELECT longest_Streak FROM Streak WHERE Habit_name= ?", (habit_name,)).fetchone()
    db.commit()
    return int(longest_streak[0])


def get_all_tracked_habits():
    cur = db.cursor()
    all_tracked_habits = cur.execute("SELECT Habit_name FROM Habit").fetchall()
    db.commit()
    return list(all_tracked_habits)

