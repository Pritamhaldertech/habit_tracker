from typing import List, Optional
from datetime import datetime
from habit_tracker.models.habit import Habit
from habit_tracker.storage.json_storage import JSONStorage


class HabitTracker:
    """Manages all habits and coordinates CRUD operations."""
    
    def __init__(self, storage: Optional[JSONStorage] = None):
        """
        Initialize the habit tracker.
        
        Args:
            storage: Storage instance (creates default if not provided)
        """
        self.storage = storage or JSONStorage()
        self.habits: List[Habit] = []
        self.load_data()
    
    def create_habit(self, name: str, periodicity: str) -> Optional[Habit]:
        """
        Create a new habit.
        
        Args:
            name: Habit name/description
            periodicity: 'daily' or 'weekly'
            
        Returns:
            The created Habit object, or None if invalid
        """
        if not name or name.strip() == "":
            return None
        
        if periodicity.lower() not in ['daily', 'weekly']:
            return None
        
        # Check if habit with same name already exists
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                return None
        
        new_habit = Habit(name, periodicity)
        self.habits.append(new_habit)
        self.save_data()
        return new_habit
    
    def delete_habit(self, habit_id: int) -> bool:
        """
        Delete a habit by its index in the list.
        
        Args:
            habit_id: Index of habit to delete (0-based)
            
        Returns:
            True if deleted, False if index invalid
        """
        if 0 <= habit_id < len(self.habits):
            deleted = self.habits.pop(habit_id)
            self.save_data()
            return True
        return False
    
    def delete_habit_by_name(self, name: str) -> bool:
        """
        Delete a habit by its name.
        
        Args:
            name: Name of habit to delete
            
        Returns:
            True if deleted, False if not found
        """
        for i, habit in enumerate(self.habits):
            if habit.name.lower() == name.lower():
                self.habits.pop(i)
                self.save_data()
                return True
        return False
    
    def check_off(self, habit_id: int, timestamp: Optional[datetime] = None) -> bool:
        """
        Check off a habit (record a completion).
        
        Args:
            habit_id: Index of habit (0-based)
            timestamp: When it was completed (defaults to now)
            
        Returns:
            True if checked off successfully, False if invalid or duplicate
        """
        if 0 <= habit_id < len(self.habits):
            result = self.habits[habit_id].add_completion(timestamp)
            if result:
                self.save_data()
            return result
        return False
    
    def get_all_habits(self) -> List[Habit]:
        """Return all habits."""
        return self.habits.copy()
    
    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """
        Return habits filtered by periodicity.
        
        Args:
            periodicity: 'daily' or 'weekly'
            
        Returns:
            List of habits with matching periodicity
        """
        return [h for h in self.habits if h.periodicity == periodicity.lower()]
    
    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        """
        Find a habit by its name.
        
        Args:
            name: Habit name to search for
            
        Returns:
            Habit object or None if not found
        """
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                return habit
        return None
    
    def get_habit_index(self, name: str) -> int:
        """
        Get the index of a habit by name.
        
        Args:
            name: Habit name to search for
            
        Returns:
            Index position or -1 if not found
        """
        for i, habit in enumerate(self.habits):
            if habit.name.lower() == name.lower():
                return i
        return -1
    
    def save_data(self) -> None:
        """Save all habits to storage."""
        habits_data = [habit.to_dict() for habit in self.habits]
        self.storage.save(habits_data)
    
    def load_data(self) -> None:
        """Load habits from storage."""
        habits_data = self.storage.load()
        self.habits = [Habit.from_dict(data) for data in habits_data]
    
    def init_predefined_habits(self) -> None:
        """
        Create 5 predefined habits with 4 weeks of example data.
        Only runs if no habits exist.
        """
        if self.habits:
            return  # Don't overwrite existing habits
        
        # Create 5 predefined habits with example completion data
        from datetime import timedelta
        
        # Predefined habit definitions
        predefined = [
            ("Daily Exercise", "daily"),
            ("Read 20 pages", "daily"),
            ("Meditate 10 minutes", "daily"),
            ("Meal plan", "weekly"),
            ("Call family", "weekly")
        ]
        
        # Start date: 4 weeks ago from today
        start_date = datetime.now() - timedelta(days=28)
        
        for name, periodicity in predefined:
            habit = Habit(name, periodicity)
            
            # Generate 4 weeks of example data
            if periodicity == "daily":
                # Daily: 28 days of completions (some with gaps for testing)
                for day in range(28):
                    check_date = start_date + timedelta(days=day)
                    
                    if name == "Daily Exercise":
                        # Perfect streak - every day
                        habit.add_completion(check_date)
                    
                    elif name == "Read 20 pages":
                        # Broken after day 5, then resumed
                        if day < 5 or day >= 14:
                            habit.add_completion(check_date)
                    
                    elif name == "Meditate 10 minutes":
                        # Every other day pattern
                        if day % 2 == 0:
                            habit.add_completion(check_date)
            
            else:  # weekly
                # Weekly: 4 weeks of completions
                for week in range(4):
                    check_date = start_date + timedelta(days=week * 7)
                    
                    if name == "Meal plan":
                        # Completed first 2 weeks, missed week 3
                        if week < 2:
                            habit.add_completion(check_date)
                    
                    elif name == "Call family":
                        # Perfect streak - all 4 weeks
                        habit.add_completion(check_date)
            
            self.habits.append(habit)
        
        self.save_data()
    
    def __len__(self) -> int:
        """Return number of habits."""
        return len(self.habits)
    
    def __repr__(self) -> str:
        return f"HabitTracker(habits={len(self.habits)})"
