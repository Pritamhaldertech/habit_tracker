import pytest
import os
import tempfile
from habit_tracker.services.tracker import HabitTracker
from habit_tracker.storage.json_storage import JSONStorage


class TestHabitTracker:
    """Unit tests for HabitTracker class."""
    
    def setup_method(self):
        """Create a fresh tracker for each test."""
        # Use temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_habits.json")
        self.storage = JSONStorage(self.test_file)
        self.tracker = HabitTracker(self.storage)
    
    def teardown_method(self):
        """Clean up after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
    
    def test_create_habit_valid(self):
        """Test creating a valid habit."""
        habit = self.tracker.create_habit("Exercise", "daily")
        assert habit is not None
        assert habit.name == "Exercise"
        assert len(self.tracker.get_all_habits()) == 1
    
    def test_create_habit_empty_name(self):
        """Test creating habit with empty name fails."""
        habit = self.tracker.create_habit("", "daily")
        assert habit is None
        assert len(self.tracker.get_all_habits()) == 0
    
    def test_create_habit_invalid_periodicity(self):
        """Test creating habit with invalid periodicity fails."""
        habit = self.tracker.create_habit("Test", "monthly")
        assert habit is None
        assert len(self.tracker.get_all_habits()) == 0
    
    def test_create_habit_duplicate_name(self):
        """Test creating duplicate habit name fails."""
        self.tracker.create_habit("Exercise", "daily")
        duplicate = self.tracker.create_habit("Exercise", "weekly")
        assert duplicate is None
        assert len(self.tracker.get_all_habits()) == 1
    
    def test_delete_habit_valid(self):
        """Test deleting a habit by index."""
        self.tracker.create_habit("Habit1", "daily")
        self.tracker.create_habit("Habit2", "weekly")
        assert len(self.tracker.get_all_habits()) == 2
        
        result = self.tracker.delete_habit(0)
        assert result == True
        assert len(self.tracker.get_all_habits()) == 1
        assert self.tracker.get_all_habits()[0].name == "Habit2"
    
    def test_delete_habit_invalid_index(self):
        """Test deleting with invalid index returns False."""
        self.tracker.create_habit("Habit1", "daily")
        result = self.tracker.delete_habit(5)
        assert result == False
        assert len(self.tracker.get_all_habits()) == 1
    
    def test_delete_habit_by_name(self):
        """Test deleting a habit by name."""
        self.tracker.create_habit("Exercise", "daily")
        result = self.tracker.delete_habit_by_name("Exercise")
        assert result == True
        assert len(self.tracker.get_all_habits()) == 0
    
    def test_check_off_valid(self):
        """Test checking off a habit."""
        self.tracker.create_habit("Exercise", "daily")
        result = self.tracker.check_off(0)
        assert result == True
        habit = self.tracker.get_all_habits()[0]
        assert len(habit.completions) == 1
    
    def test_check_off_invalid_index(self):
        """Test checking off with invalid index returns False."""
        result = self.tracker.check_off(99)
        assert result == False
    
    def test_get_all_habits(self):
        """Test getting all habits."""
        self.tracker.create_habit("Habit1", "daily")
        self.tracker.create_habit("Habit2", "weekly")
        all_habits = self.tracker.get_all_habits()
        assert len(all_habits) == 2
    
    def test_get_habits_by_periodicity(self):
        """Test filtering habits by periodicity."""
        self.tracker.create_habit("Daily1", "daily")
        self.tracker.create_habit("Daily2", "daily")
        self.tracker.create_habit("Weekly1", "weekly")
        
        daily = self.tracker.get_habits_by_periodicity("daily")
        weekly = self.tracker.get_habits_by_periodicity("weekly")
        
        assert len(daily) == 2
        assert len(weekly) == 1
    
    def test_save_and_load_data(self):
        """Test that data persists after save/load."""
        self.tracker.create_habit("Persistent", "daily")
        self.tracker.check_off(0)
        
        # Create new tracker with same storage
        new_tracker = HabitTracker(self.storage)
        assert len(new_tracker.get_all_habits()) == 1
        habit = new_tracker.get_all_habits()[0]
        assert habit.name == "Persistent"
        assert len(habit.completions) == 1
    
    def test_init_predefined_habits(self):
        """Test that predefined habits are created when no habits exist."""
        assert len(self.tracker.get_all_habits()) == 0
        self.tracker.init_predefined_habits()
        assert len(self.tracker.get_all_habits()) == 5
    
    def test_len(self):
        """Test __len__ method."""
        assert len(self.tracker) == 0
        self.tracker.create_habit("Test", "daily")
        assert len(self.tracker) == 1
