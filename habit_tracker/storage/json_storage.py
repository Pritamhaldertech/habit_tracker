import json
import os
from typing import List, Dict, Any
from datetime import datetime


class JSONStorage:
    """Handles all JSON file operations for habit persistence."""
    
    def __init__(self, file_path: str = "data/habits.json"):
        """
        Initialize storage with a file path.
        
        Args:
            file_path: Path to the JSON file (default: data/habits.json)
        """
        self.file_path = file_path
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """Create the data directory if it doesn't exist."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save(self, habits_data: List[Dict[str, Any]]) -> None:
        """
        Save habits data to JSON file.
        
        Args:
            habits_data: List of habit dictionaries to save
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'habits': habits_data,
                'metadata': {
                    'version': '1.0',
                    'last_saved': datetime.now().isoformat(),
                    'habit_count': len(habits_data)
                }
            }, f, indent=2, ensure_ascii=False)
    
    def load(self) -> List[Dict[str, Any]]:
        """
        Load habits data from JSON file.
        
        Returns:
            List of habit dictionaries, or empty list if file doesn't exist or is corrupted
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('habits', [])
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            # Return empty list if file is corrupted or has wrong structure
            return []
    
    def delete_data_file(self) -> bool:
        """
        Delete the data file (useful for testing).
        
        Returns:
            True if deleted, False if file didn't exist
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            return True
        return False
