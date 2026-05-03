# Habit Tracker App

A Python-based habit tracking application with OOP design and functional analytics.

## Features

- Create daily or weekly habits
- Check off completions
- Automatic streak calculation (respects periodicity)
- Analytics dashboard with pure functions
- JSON file storage (no database needed)
- 5 predefined habits with 4 weeks of example data
- 38 unit tests with pytest

## Installation

```bash
git clone https://github.com/Pritamhaldertech/habit_tracker.git
cd habit_tracker
pip install -r requirements.txt

## Usage
Run the application:
bash python3 main.py

## Main Menu Options
text
----------------------------------------
MAIN MENU
----------------------------------------
1. Create new habit
2. Check off habit (complete task)
3. View all habits
4. View habits by periodicity
5. Analytics dashboard
6. Delete habit
7. Save & Exit
----------------------------------------
## Screenshots
Main menu: <img width="795" height="443" alt="Screenshot 2026-05-03 at 11 26 07" src="https://github.com/user-attachments/assets/a4ff449d-6d52-490c-8423-09d7ed314b29" />
Analytics Dashboard: <img width="1131" height="914" alt="Screenshot 2026-05-03 at 11 27 33" src="https://github.com/user-attachments/assets/2fa9f8ca-2f0f-4a73-96d8-59821cd06b78" />
Unit Test results: <img width="922" height="627" alt="Screenshot 2026-05-03 at 11 28 39" src="https://github.com/user-attachments/assets/a59e229c-5013-4239-8cf7-3ff97d74a0cc" />
UML class diagram: <img width="1115" height="564" alt="Screenshot 2026-05-03 at 10 36 24" src="https://github.com/user-attachments/assets/654b4c6f-2e1c-4c34-b222-f537f9b5c430" />

## How to Use
Create a Habit
Select option 1 from main menu

Enter habit name (e.g., "Exercise")

Choose periodicity: 1 for Daily or 2 for Weekly

Habit is saved automatically

Check Off a Habit
Select option 2 from main menu

Choose habit number from the list

Confirm completion

System shows your current streak

## View Analytics
Select option 5 from main menu

View:

Total habits tracked

Longest streak across all habits

Longest streak for each habit

Broken habits

Active streaks leaderboard

Analytics Functions (Functional Programming)
The analytics module uses pure functions with no side effects:
1. List comprehension: get_all_habits_list(); Returns list of all habit names
2. filter() + lambda: filter_by_periodicity();	Filters habits by daily/weekly
3. map() + max(): longest_streak_all(); Finds longest streak across all habits
4. Pure function lookup: longest_streak_for_habit(); Longest streak for a specific habit
5. map() + dict(): get_streak_summary(); Returns streak summary dictionary
6. filter() + map(): get_broken_habits(); Lists habits broken in current period
7. filter() + sorted(): get_active_streaks(); Returns active streaks sorted

Running Tests: python3 -m pytest tests/ -v
Expected output: 38 passed in 0.10s

habit_tracker/
├── models/
│   └── habit.py              # Habit class (OOP)
├── services/
│   ├── tracker.py            # CRUD operations
│   └── analytics.py          # Pure functions (Functional Programming)
├── storage/
│   └── json_storage.py       # JSON persistence
├── cli.py                    # Menu interface
└── main.py                   # Entry point

tests/
├── test_habit.py             # Habit class tests
├── test_tracker.py           # Tracker tests
├── test_analytics.py         # Analytics tests
└── test_storage.py           # Storage tests

data/
└── habits.json               # Stored habit data (auto-created)

screenshots/                  # Screenshots for documentation

Predefined Habits (Test Fixture)
On first run, 5 habits are automatically created with 4 weeks of example data:

#	Habit Name	Periodicity	Test Data Pattern
1	Habit name: Daily Exercise|	Periodicty: Daily|	Test data pattern: Perfect streak (every day for 28 days)
2	Habit name: Read 20 pages|	Periodicity: Daily|	Test data pattern: Broken after day 5, then resumed
3	Habit name: Meditate 10 minutes|	Periodicity: Daily| Test data pattern: Every other day pattern
4	Habit name: Meal plan| Periodicity:	Weekly| Test data pattern:	Weeks 1-2 completed, missed week 3
5	Habit name: Call family	| Periodicity: Weekly	| Test data pattern: All 4 weeks completed (streak = 4)

## Data Persistence
Format: JSON (using Python's built-in json module)
Location: data/habits.json
Save trigger: After every create, check-off, or delete operation
Load trigger: On application startup

## Streak Calculation Logic
Daily Habits
Each calendar day = 1 period
Must complete at least once per day
Miss one day = streak breaks

## Weekly Habits
Each week (Monday-Sunday) = 1 period
Must complete at least once per week
Miss one week = streak breaks

## Algorithm
Sort completions chronologically
Group by period (day for daily, week for weekly)
Count backwards from most recent period
Stop when period with no completion is found

## Acceptance Criteria Met
Python 3.7+ compatible
Habit class using OOP
Daily and weekly periodicities
5 predefined habits with 4 weeks of example data
JSON file persistence
Analytics module with functional programming (pure functions)

CLI menu-driven interface
Unit tests with pytest (38 tests passing)
Docstrings and code comments
Modular project structure

## Technologies Used
Python 3.9+
pytest (testing)
JSON (data storage)
No external dependencies (except pytest for development)
