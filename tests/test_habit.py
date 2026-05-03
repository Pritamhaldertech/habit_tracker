import pytest
from datetime import datetime, timedelta
from habit_tracker.models.habit import Habit


class TestHabit:
    """Unit tests for Habit class."""
    
    def test_create_habit_valid(self):
        """Test creating a habit with valid inputs."""
        habit = Habit("Test Habit", "daily")
        assert habit.name == "Test Habit"
        assert habit.periodicity == "daily"
        assert len(habit.completions) == 0
        assert habit.created_at is not None
    
    def test_create_habit_weekly(self):
        """Test creating a weekly habit."""
        habit = Habit("Weekly Test", "weekly")
        assert habit.periodicity == "weekly"
    
    def test_create_habit_with_completions(self):
        """Test creating a habit with existing completions."""
        completions = [datetime.now()]
        habit = Habit("Test", "daily", completions=completions)
        assert len(habit.completions) == 1
    
    def test_add_completion(self):
        """Test adding a completion to a habit."""
        habit = Habit("Test", "daily")
        result = habit.add_completion()
        assert result == True
        assert len(habit.completions) == 1
    
    def test_add_completion_duplicate_same_day(self):
        """Test that duplicate completions on same day are prevented."""
        habit = Habit("Test", "daily")
        timestamp = datetime(2026, 5, 1, 10, 0, 0)
        habit.add_completion(timestamp)
        result = habit.add_completion(timestamp)
        assert result == False
        assert len(habit.completions) == 1
    
    def test_add_completion_different_days_allowed(self):
        """Test that completions on different days are allowed."""
        habit = Habit("Test", "daily")
        habit.add_completion(datetime(2026, 5, 1, 10, 0, 0))
        result = habit.add_completion(datetime(2026, 5, 2, 10, 0, 0))
        assert result == True
        assert len(habit.completions) == 2
    
    def test_to_dict(self):
        """Test converting habit to dictionary."""
        habit = Habit("Test", "daily")
        habit.add_completion(datetime(2026, 5, 1, 10, 0, 0))
        data = habit.to_dict()
        assert data['name'] == "Test"
        assert data['periodicity'] == "daily"
        assert 'created_at' in data
        assert 'completions' in data
        assert len(data['completions']) == 1
    
    def test_from_dict(self):
        """Test creating habit from dictionary."""
        data = {
            'name': 'Test',
            'periodicity': 'daily',
            'created_at': '2026-05-01T10:00:00',
            'completions': ['2026-05-01T10:00:00']
        }
        habit = Habit.from_dict(data)
        assert habit.name == "Test"
        assert habit.periodicity == "daily"
        assert len(habit.completions) == 1
    
    def test_is_broken_no_completions(self):
        """Test that habit with no completions is broken."""
        habit = Habit("Test", "daily")
        assert habit.is_broken() == True
    
    def test_repr(self):
        """Test string representation."""
        habit = Habit("Test", "daily")
        repr_str = repr(habit)
        assert "Test" in repr_str
        assert "daily" in repr_str
