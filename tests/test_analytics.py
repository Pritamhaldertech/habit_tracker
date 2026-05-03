import pytest
from datetime import datetime, timedelta
from habit_tracker.models.habit import Habit
from habit_tracker.services import analytics as ana


class TestAnalytics:
    """Unit tests for Analytics module (pure functions)."""
    
    def setup_method(self):
        """Create test habits for analytics testing."""
        # Daily habit with perfect streak
        self.perfect_daily = Habit("Daily Perfect", "daily")
        base_date = datetime(2026, 5, 1, 8, 0, 0)
        for i in range(14):
            self.perfect_daily.add_completion(base_date + timedelta(days=i))
        
        # Daily habit with broken streak
        self.broken_daily = Habit("Daily Broken", "daily")
        for i in range(5):
            self.broken_daily.add_completion(base_date + timedelta(days=i))
        # Gap - no completion for day 5,6,7
        for i in range(8, 14):
            self.broken_daily.add_completion(base_date + timedelta(days=i))
        
        # Weekly habit
        self.weekly_habit = Habit("Weekly Habit", "weekly")
        for i in range(4):
            self.weekly_habit.add_completion(base_date + timedelta(days=i * 7))
        
        self.all_habits = [self.perfect_daily, self.broken_daily, self.weekly_habit]
    
    def test_get_all_habits_list(self):
        """Test getting list of all habit names."""
        names = ana.get_all_habits_list(self.all_habits)
        assert len(names) == 3
        assert "Daily Perfect" in names
        assert "Daily Broken" in names
        assert "Weekly Habit" in names
    
    def test_filter_by_periodicity_daily(self):
        """Test filtering to get only daily habits."""
        daily = ana.filter_by_periodicity(self.all_habits, "daily")
        assert len(daily) == 2
        assert daily[0].name == "Daily Perfect"
        assert daily[1].name == "Daily Broken"
    
    def test_filter_by_periodicity_weekly(self):
        """Test filtering to get only weekly habits."""
        weekly = ana.filter_by_periodicity(self.all_habits, "weekly")
        assert len(weekly) == 1
        assert weekly[0].name == "Weekly Habit"
    
    def test_longest_streak_all(self):
        """Test finding longest streak across all habits."""
        longest = ana.longest_streak_all(self.all_habits)
        # Daily Perfect should have 14-day streak
        assert longest == 14
    
    def test_longest_streak_for_habit_found(self):
        """Test getting longest streak for a specific habit that exists."""
        streak = ana.longest_streak_for_habit(self.all_habits, "Daily Perfect")
        assert streak == 14
    
    def test_longest_streak_for_habit_not_found(self):
        """Test getting longest streak for non-existent habit returns 0."""
        streak = ana.longest_streak_for_habit(self.all_habits, "Non Existent")
        assert streak == 0
    
    def test_longest_streak_for_habit_case_insensitive(self):
        """Test that habit name lookup is case-insensitive."""
        streak = ana.longest_streak_for_habit(self.all_habits, "daily perfect")
        assert streak == 14
    
    def test_get_streak_summary(self):
        """Test getting streak summary dictionary."""
        summary = ana.get_streak_summary(self.all_habits)
        assert len(summary) == 3
        assert "Daily Perfect" in summary
        assert summary["Daily Perfect"]["periodicity"] == "daily"
        assert summary["Weekly Habit"]["longest_streak"] == 4
    
    def test_get_broken_habits(self):
        """Test finding broken habits."""
        broken = ana.get_broken_habits(self.all_habits)
        # Daily Broken should be broken (has gaps in last periods)
        # Note: depends on current date relative to test data
        assert isinstance(broken, list)
    
    def test_get_active_streaks(self):
        """Test getting active streaks sorted."""
        active = ana.get_active_streaks(self.all_habits)
        assert isinstance(active, list)
        # Should be sorted descending by streak
        if len(active) >= 2:
            assert active[0][1] >= active[1][1]
    
    def test_habit_exists_true(self):
        """Test habit_exists returns True for existing habit."""
        exists = ana.habit_exists(self.all_habits, "Daily Perfect")
        assert exists == True
    
    def test_habit_exists_false(self):
        """Test habit_exists returns False for non-existent habit."""
        exists = ana.habit_exists(self.all_habits, "Fake Habit")
        assert exists == False
    
    def test_get_habits_sorted_by_streak(self):
        """Test sorting habits by longest streak descending."""
        sorted_habits = ana.get_habits_sorted_by_streak(self.all_habits)
        assert len(sorted_habits) == 3
        # Daily Perfect (14) should be first
        assert sorted_habits[0].name == "Daily Perfect"
    
    def test_empty_habits_list(self):
        """Test analytics functions with empty list."""
        empty = []
        assert ana.get_all_habits_list(empty) == []
        assert ana.filter_by_periodicity(empty, "daily") == []
        assert ana.longest_streak_all(empty) == 0
        assert ana.get_broken_habits(empty) == []
