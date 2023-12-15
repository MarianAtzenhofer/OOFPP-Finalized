import pytest
from main import Habit
from db import get_db, add_new_habit, complete_habit, get_longest_streak_given_habit, get_all_tracked_habits, get_streak_given_habit, reset_streak, del_habit


class TestClass:

    def setup_method(self):
        self.db = get_db("test.db")
        add_new_habit("test_habit", "daily", "test_description")




    def test_updating_streak(self):
        complete_habit("test_habit")
        complete_habit("test_habit")
        complete_habit("test_habit")
        complete_habit("test_habit")
        complete_habit("test_habit")
        reset_streak("test_habit")
        complete_habit("test_habit")


        current_streak = get_streak_given_habit("test_habit")

        assert current_streak == 1

        longest_streak = get_longest_streak_given_habit("test_habit")

        assert longest_streak == 5


    def test_resetting_streak(self):
        reset_streak("test_habit")

        current_streak = get_streak_given_habit("test_habit")
        assert current_streak == 0


    def test_del_data(self):
        del_habit("test_habit")
        test_habit = "test_habit"
        tracked_habits = get_all_tracked_habits()
        assert test_habit not in tracked_habits


    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test.db")


    if __name__ == "__main__":
        pytest.main()