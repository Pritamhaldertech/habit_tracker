from typing import List
from habit_tracker.models.habit import Habit


# ============================================
# ANALYTICS MODULE - PURE FUNCTIONS ONLY
# No side effects, no state modification
# Functional programming paradigm
# ============================================

def get_all_habits_list(habits: List[Habit]) -> List[str]:
    """
    Return a list of all habit names.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of habit names as strings
        
    Example:
        >>> get_all_habits_list([habit1, habit2])
        ['Daily Exercise', 'Read 20 pages']
    """
    return list(map(lambda h: h.name, habits))


def filter_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    Filter habits by periodicity using functional filter.
    
    Args:
        habits: List of Habit objects
        periodicity: 'daily' or 'weekly'
        
    Returns:
        List of habits matching the periodicity
        
    Example:
        >>> filter_by_periodicity(habits, 'daily')
        [Habit(name='Daily Exercise', ...), Habit(name='Read 20 pages', ...)]
    """
    return list(filter(lambda h: h.periodicity == periodicity.lower(), habits))


def longest_streak_all(habits: List[Habit]) -> int:
    """
    Find the longest streak across all habits using map() and max().
    
    Args:
        habits: List of Habit objects
        
    Returns:
        Maximum streak length found (0 if no habits)
        
    Example:
        >>> longest_streak_all(habits)
        14  # 14-day streak from Daily Exercise
    """
    if not habits:
        return 0
    
    streaks = list(map(lambda h: h.longest_streak(), habits))
    return max(streaks, default=0)


def longest_streak_for_habit(habits: List[Habit], name: str) -> int:
    """
    Find the longest streak for a specific habit by name.
    
    Args:
        habits: List of Habit objects
        name: Name of the habit to look up (case-insensitive)
        
    Returns:
        Longest streak for that habit, or 0 if habit not found
        
    Example:
        >>> longest_streak_for_habit(habits, 'Daily Exercise')
        14
    """
    # Find matching habit using filter
    matching = list(filter(lambda h: h.name.lower() == name.lower(), habits))
    
    if not matching:
        return 0
    
    return matching[0].longest_streak()


def get_streak_summary(habits: List[Habit]) -> dict:
    """
    Get a summary of streaks for all habits.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        Dictionary with habit names as keys and streak info as values
    """
    return dict(map(lambda h: (h.name, {
        'current_streak': h.current_streak(),
        'longest_streak': h.longest_streak(),
        'periodicity': h.periodicity
    }), habits))


def get_broken_habits(habits: List[Habit]) -> List[str]:
    """
    Get list of habits that are currently broken.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of habit names that are broken in the current period
    """
    return list(map(lambda h: h.name, filter(lambda h: h.is_broken(), habits)))


def get_active_streaks(habits: List[Habit]) -> List[tuple]:
    """
    Get all habits with their current streak lengths, sorted by streak.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of tuples (habit_name, current_streak) sorted descending
    """
    active = list(filter(lambda h: h.current_streak() > 0, habits))
    with_streaks = list(map(lambda h: (h.name, h.current_streak()), active))
    return sorted(with_streaks, key=lambda x: x[1], reverse=True)


def habit_exists(habits: List[Habit], name: str) -> bool:
    """
    Check if a habit exists by name.
    
    Args:
        habits: List of Habit objects
        name: Habit name to check
        
    Returns:
        True if habit exists, False otherwise
    """
    return len(list(filter(lambda h: h.name.lower() == name.lower(), habits))) > 0


def get_habits_sorted_by_streak(habits: List[Habit]) -> List[Habit]:
    """
    Return habits sorted by their longest streak (descending).
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of habits sorted by longest streak
    """
    return sorted(habits, key=lambda h: h.longest_streak(), reverse=True)
