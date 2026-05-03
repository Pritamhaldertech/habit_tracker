from datetime import datetime
from typing import List, Optional


class Habit:
    """Represents a single habit tracked by the user."""
    
    def __init__(self, name: str, periodicity: str, created_at: Optional[datetime] = None, completions: Optional[List[datetime]] = None):
        """
        Initialize a new habit.
        
        Args:
            name: Habit name/description
            periodicity: 'daily' or 'weekly'
            created_at: Creation timestamp (defaults to now)
            completions: List of completion timestamps (defaults to empty list)
        """
        self.name = name
        self.periodicity = periodicity.lower()
        self.created_at = created_at or datetime.now()
        self.completions = completions or []
    
    def add_completion(self, timestamp: Optional[datetime] = None) -> bool:
        """
        Record a completion of this habit.
        
        Args:
            timestamp: When the habit was completed (defaults to now)
            
        Returns:
            True if completion was added, False if duplicate for this period
        """
        timestamp = timestamp or datetime.now()
        
        # Prevent duplicate completion in same period
        if self._has_completion_in_period(timestamp):
            return False
        
        self.completions.append(timestamp)
        return True
    
    def _has_completion_in_period(self, timestamp: datetime) -> bool:
        """Check if there's already a completion in the same period."""
        for completion in self.completions:
            if self._same_period(completion, timestamp):
                return True
        return False
    
    def _same_period(self, date1: datetime, date2: datetime) -> bool:
        """Check if two datetimes are in the same period (day or week)."""
        if self.periodicity == 'daily':
            return date1.date() == date2.date()
        else:  # weekly
            # Compare year and week number
            return date1.isocalendar()[:2] == date2.isocalendar()[:2]
    
    def current_streak(self) -> int:
        """
        Calculate the current active streak.
        
        Returns:
            Number of consecutive periods completed (counting backwards from most recent)
        """
        if not self.completions:
            return 0
        
        sorted_completions = sorted(self.completions)
        streak = 0
        current_date = datetime.now()
        
        # Check from most recent backwards
        for i in range(len(sorted_completions) - 1, -1, -1):
            if self._is_in_period(sorted_completions[i], current_date):
                streak += 1
                # Move to previous period
                current_date = self._previous_period(current_date)
            else:
                break
        
        return streak
    
    def _is_in_period(self, completion_date: datetime, period_date: datetime) -> bool:
        """Check if completion falls within the given period."""
        if self.periodicity == 'daily':
            return completion_date.date() == period_date.date()
        else:  # weekly
            return completion_date.isocalendar()[:2] == period_date.isocalendar()[:2]
    
    def _previous_period(self, date: datetime) -> datetime:
        """Get the start of the previous period."""
        if self.periodicity == 'daily':
            # Subtract 1 day
            from datetime import timedelta
            return date - timedelta(days=1)
        else:  # weekly
            # Subtract 7 days
            from datetime import timedelta
            return date - timedelta(days=7)
    
    def longest_streak(self) -> int:
        """
        Calculate the longest streak ever achieved.
        
        Returns:
            Maximum consecutive periods completed
        """
        if not self.completions:
            return 0
        
        sorted_completions = sorted(self.completions)
        longest = 1
        current = 1
        
        for i in range(1, len(sorted_completions)):
            if self._consecutive_periods(sorted_completions[i-1], sorted_completions[i]):
                current += 1
            else:
                longest = max(longest, current)
                current = 1
        
        return max(longest, current)
    
    def _consecutive_periods(self, date1: datetime, date2: datetime) -> bool:
        """Check if two completions are in consecutive periods."""
        if self.periodicity == 'daily':
            return (date2.date() - date1.date()).days == 1
        else:  # weekly
            year1, week1, _ = date1.isocalendar()
            year2, week2, _ = date2.isocalendar()
            
            if year1 == year2:
                return week2 - week1 == 1
            elif year2 == year1 + 1:
                return week1 == 52 and week2 == 1
            return False
    
    def is_broken(self) -> bool:
        """Check if the habit was broken in the current period."""
        if not self.completions:
            return True
        return not self._has_completion_in_period(datetime.now())
    
    def to_dict(self) -> dict:
        """Convert habit to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'periodicity': self.periodicity,
            'created_at': self.created_at.isoformat(),
            'completions': [c.isoformat() for c in self.completions]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Habit':
        """Create a Habit instance from a dictionary."""
        habit = cls(
            name=data['name'],
            periodicity=data['periodicity'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
        habit.completions = [datetime.fromisoformat(c) for c in data.get('completions', [])]
        return habit
    
    def __repr__(self) -> str:
        return f"Habit(name='{self.name}', periodicity='{self.periodicity}', completions={len(self.completions)})"
