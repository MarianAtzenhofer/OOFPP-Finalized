import questionary
from main import Streak
from main import Habit
from main import Timespan
from db import get_unchecked_habits
from db import del_habit
from db import complete_habit
from db import reset_streak
from db import get_all_tracked_habits
from db import get_all_habits_same_periodicity
from db import get_longest_streak_given_habit
from db import get_highest_streak
from db import get_db
from db import add_new_habit


db = get_db()


def cli():
    while True:
        choice = questionary.select(f"What do you want to do?",
                                    choices=["Create Habit", "analyse habits", "manage habits", "Quit"]).ask()
        if choice == "Quit":
            break

        if choice == "Create Habit":
            habit_name = questionary.text(f"Name the Habit you want to create").ask()
            while True:
                if habit_name:
                    description = questionary.text(f"Please describe your habit. This is optional.").ask()
                    timespan = questionary.select(f"Please specify the timespan",
                                                  choices=["weekly", "daily"]).ask()
                    add_new_habit(habit_name, timespan, description)
                    questionary.text(
                        "your Habit is no being tracked! \n Your Streak starts now! \n Press Enter to continue.").ask()

                    break
                else:
                    print("Ops, seems like you forgot to enter a habit name.")
                    retry_choice = questionary.select("Do you want to try again?",
                                                      choices=["Try Again", "Exit"]).ask()

                    if retry_choice == "Exit":
                        break
                    elif retry_choice == "Try Again":
                        habit_name = questionary.text(f"Name the Habit you want to create").ask()

        elif choice == "analyse habits":
            choice = questionary.select(f"What would you like to know about your habits?",
                               choices=["return a list of all currently tracked habits",
                                        "returning a list of all habits with the same timespan",
                                        "return the longest run streak of all defined habits",
                                        "returning the longest run streak for a given habit",
                                        ]).ask()
            if choice == "return a list of all currently tracked habits":
                all_habits = get_all_tracked_habits()
                questionary.text(f"Here is a list of all currently tracked habits: {all_habits} "
                                 f"\n Press Enter to continue.").ask()

            elif choice == "returning a list of all habits with the same timespan":
                timespan = questionary.select(f"please clarify timespan.",
                                            choices=["weekly", "daily"]).ask()
                same_timespan = get_all_habits_same_periodicity(timespan)
                questionary.text(f"Here is a list of all tracked Habits with the same timespan: {same_timespan}"
                                 f"\n Press Enter to continue.").ask()

            elif choice == "return the longest run streak of all defined habits":
                longest_streak_all_habits = get_highest_streak()
                questionary.text(
                    f"Here is the longest streak of all your tracked Habits: {longest_streak_all_habits}"
                    f"\n Press Enter to continue.").ask()  # habit_name??

            elif choice == "returning the longest run streak for a given habit":
                habit_name = questionary.text(f"please specify habit name").ask()
                all_habits_tuple = get_all_tracked_habits()
                while True:
                    if any(habit_name in habit_tuple for habit_tuple in all_habits_tuple):
                        longest_streak_given_habit = get_longest_streak_given_habit(habit_name)
                        questionary.text(
                            f"Here is the longest Streak you ever accomplished for {habit_name}: "
                            f"{longest_streak_given_habit}"
                            f"\n Press Enter to continue.").ask()
                        break
                    else:
                        print("Ops, seems like there is no habit with that name.")
                        retry_choice = questionary.select("Do you want to try giving another name "
                                                          "or do you wish to exit?",
                                                          choices=["Try Again", "Exit"]).ask()

                        if retry_choice == "Exit":
                            break
                        elif retry_choice == "Try Again":
                            habit_name = questionary.text(f"Name the Habit again please").ask()


        elif choice == "manage habits":
            choice = questionary.select(f"what would you like to do?",
                               choices=["delete a habit", "check off a habit", "show unchecked Habits"]).ask()

            if choice == "delete a habit":
                all_habits_tuple = get_all_tracked_habits()
                habit_name = questionary.text(f"Name the Habit you want to delete").ask()
                while True:
                    if any(habit_name in habit_tuple for habit_tuple in all_habits_tuple):
                        del_habit(habit_name)
                        questionary.text("Your habit has been deleted."
                                         "\n Press Enter to continue.").ask()
                        break
                    else:
                        print("Ops, seems like there is no habit with that name.")
                        retry_choice = questionary.select("Do you want to try giving another name "
                                                          "or do you wish to exit?",
                                                      choices=["Try Again", "Exit"]).ask()

                        if retry_choice == "Exit":
                            break
                        elif retry_choice == "Try Again":
                            habit_name = questionary.text(f"Name the Habit you want to delete").ask()

            elif choice == "check off a habit":
                all_habits_tuple = get_all_tracked_habits()
                habit_name = questionary.text(f"Please give the name of the habit you would like to check off").ask()
                while True:
                    if any(habit_name in habit_tuple for habit_tuple in all_habits_tuple):
                        streak = Streak(habit_name)
                        streak_update = streak.update_streak(habit_name)
                        if streak_update == "Your streak has been incremented! Keep it up!":
                            questionary.text(f"{streak_update} \n Press Enter to Continue.").ask()
                            complete_habit(habit_name)
                            break
                        else:
                            questionary.text(f"Sadly, you have failed to keep up this streak.").ask()
                            choice = questionary.select("Do you want to start over?", choices=["Yes", "No"]).ask()
                            if choice == "Yes":
                                reset_streak(habit_name)
                                questionary.text("Your Habit is being tracked. Remember to check it off!"
                                                 "\n Press Enter to continue").ask()
                                break
                            else:
                                break
                    else:
                        print("Ops, seems like there is no habit with that name.")
                        retry_choice = questionary.select("Do you want to try again or exit?",
                                                          choices=["Try Again", "Exit"]).ask()

                        if retry_choice == "Exit":
                            break
                        elif retry_choice == "Try Again":
                            habit_name = questionary.text(f"Name the Habit you want to check off").ask()

            elif choice == "show unchecked Habits":
                unchecked_habits = get_unchecked_habits()
                questionary.text(f"These are all uncompleted Habits: {unchecked_habits}"
                                 f"\n Press Enter to continue.").ask()


if __name__ == "__main__":
    cli()










