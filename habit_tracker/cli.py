from habit_tracker.services.tracker import HabitTracker
from habit_tracker.services import analytics as ana


class CLI:
    """Command-line interface for the Habit Tracker application."""
    
    def __init__(self):
        """Initialize the CLI with a HabitTracker instance."""
        self.tracker = HabitTracker()
    
    def run(self) -> None:
        """Start the main application loop."""
        print("\n" + "=" * 50)
        print("   HABIT TRACKER - Welcome Back!")
        print("=" * 50)
        
        # Initialize predefined habits if no habits exist
        if len(self.tracker) == 0:
            print("\n📌 First time setup: Creating 5 predefined habits with 4 weeks of example data...")
            self.tracker.init_predefined_habits()
            print("✅ Done! You can now track these habits.\n")
        
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.create_habit()
            elif choice == '2':
                self.check_off_habit()
            elif choice == '3':
                self.view_all_habits()
            elif choice == '4':
                self.view_habits_by_periodicity()
            elif choice == '5':
                self.analytics_dashboard()
            elif choice == '6':
                self.delete_habit()
            elif choice == '7':
                self.save_and_exit()
                break
            elif choice == '8':
                self.save_and_exit()
                break
            else:
                print("❌ Invalid choice. Please enter 1-8.")
    
    def display_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "-" * 40)
        print("MAIN MENU")
        print("-" * 40)
        print("1. Create new habit")
        print("2. Check off habit (complete task)")
        print("3. View all habits")
        print("4. View habits by periodicity")
        print("5. Analytics dashboard")
        print("6. Delete habit")
        print("7. Save & Exit")
        print("-" * 40)
    
    def create_habit(self) -> None:
        """Create a new habit."""
        print("\n--- CREATE NEW HABIT ---")
        
        name = input("Habit name: ").strip()
        if not name:
            print("❌ Habit name cannot be empty.")
            return
        
        print("Periodicity:")
        print("  1. Daily")
        print("  2. Weekly")
        period_choice = input("Choose (1 or 2): ").strip()
        
        if period_choice == '1':
            periodicity = 'daily'
        elif period_choice == '2':
            periodicity = 'weekly'
        else:
            print("❌ Invalid choice.")
            return
        
        habit = self.tracker.create_habit(name, periodicity)
        if habit:
            print(f"✅ Habit '{name}' created successfully with {periodicity} periodicity!")
        else:
            print(f"❌ Could not create habit. Name may already exist or be invalid.")
    
    def check_off_habit(self) -> None:
        """Check off a habit (record a completion)."""
        print("\n--- CHECK OFF HABIT ---")
        
        habits = self.tracker.get_all_habits()
        if not habits:
            print("❌ No habits found. Create one first.")
            return
        
        print("\nSelect habit to check off:")
        for i, habit in enumerate(habits):
            print(f"  {i+1}. {habit.name} ({habit.periodicity}) - Current streak: {habit.current_streak()}")
        
        try:
            choice = int(input("\nEnter habit number: ")) - 1
            if 0 <= choice < len(habits):
                success = self.tracker.check_off(choice)
                if success:
                    habit = self.tracker.get_all_habits()[choice]
                    print(f"✅ Checked off '{habit.name}'!")
                    print(f"   Current streak: {habit.current_streak()} periods")
                else:
                    print("❌ Could not check off. You may have already completed this habit in this period.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def view_all_habits(self) -> None:
        """Display all habits with their details."""
        print("\n--- ALL HABITS ---")
        
        habits = self.tracker.get_all_habits()
        if not habits:
            print("No habits found. Create one using option 1.")
            return
        
        print("\n" + "-" * 60)
        print(f"{'#':<3} {'Name':<20} {'Periodicity':<10} {'Completions':<12} {'Current Streak':<15}")
        print("-" * 60)
        
        for i, habit in enumerate(habits):
            print(f"{i+1:<3} {habit.name:<20} {habit.periodicity:<10} {len(habit.completions):<12} {habit.current_streak():<15}")
        print("-" * 60)
    
    def view_habits_by_periodicity(self) -> None:
        """View habits filtered by daily or weekly."""
        print("\n--- VIEW HABITS BY PERIODICITY ---")
        print("1. Daily habits")
        print("2. Weekly habits")
        
        choice = input("Choose (1 or 2): ").strip()
        
        if choice == '1':
            periodicity = 'daily'
        elif choice == '2':
            periodicity = 'weekly'
        else:
            print("❌ Invalid choice.")
            return
        
        habits = self.tracker.get_habits_by_periodicity(periodicity)
        
        if not habits:
            print(f"\nNo {periodicity} habits found.")
            return
        
        print(f"\n--- {periodicity.upper()} HABITS ---")
        for i, habit in enumerate(habits):
            print(f"  {i+1}. {habit.name} - Completions: {len(habit.completions)}")
    
    def analytics_dashboard(self) -> None:
        """Display analytics dashboard using functional analytics module."""
        print("\n" + "=" * 50)
        print("   ANALYTICS DASHBOARD")
        print("=" * 50)
        
        habits = self.tracker.get_all_habits()
        
        if not habits:
            print("\n❌ No habits to analyze. Create some first.")
            return
        
        # Using functional analytics functions
        print("\n📊 HABIT SUMMARY")
        print("-" * 40)
        
        all_names = ana.get_all_habits_list(habits)
        print(f"Total habits tracked: {len(all_names)}")
        
        daily_habits = ana.filter_by_periodicity(habits, 'daily')
        weekly_habits = ana.filter_by_periodicity(habits, 'weekly')
        print(f"Daily habits: {len(daily_habits)}")
        print(f"Weekly habits: {len(weekly_habits)}")
        
        print("\n🏆 STREAK LEADERBOARD")
        print("-" * 40)
        
        longest_overall = ana.longest_streak_all(habits)
        print(f"Longest streak across ALL habits: {longest_overall} periods")
        
        print("\nLongest streak for each habit:")
        for habit in habits:
            streak = ana.longest_streak_for_habit(habits, habit.name)
            print(f"  • {habit.name}: {streak} periods ({habit.periodicity})")
        
        print("\n⚠️ BROKEN HABITS")
        print("-" * 40)
        broken = ana.get_broken_habits(habits)
        if broken:
            for habit_name in broken:
                print(f"  • {habit_name}")
        else:
            print("  No broken habits! Great job!")
        
        print("\n🔥 ACTIVE STREAKS")
        print("-" * 40)
        active = ana.get_active_streaks(habits)
        if active:
            for name, streak in active:
                print(f"  • {name}: {streak} periods")
        else:
            print("  No active streaks. Start checking off your habits!")
        
        print("\n" + "=" * 50)
        input("Press Enter to continue...")
    
    def delete_habit(self) -> None:
        """Delete a habit."""
        print("\n--- DELETE HABIT ---")
        
        habits = self.tracker.get_all_habits()
        if not habits:
            print("❌ No habits to delete.")
            return
        
        print("\nSelect habit to delete:")
        for i, habit in enumerate(habits):
            print(f"  {i+1}. {habit.name} ({habit.periodicity})")
        
        try:
            choice = int(input("\nEnter habit number: ")) - 1
            if 0 <= choice < len(habits):
                habit_name = habits[choice].name
                confirm = input(f"Are you sure you want to delete '{habit_name}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.tracker.delete_habit(choice)
                    print(f"✅ Habit '{habit_name}' deleted.")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def save_and_exit(self) -> None:
        """Save data and exit the application."""
        print("\n💾 Saving data...")
        self.tracker.save_data()
        print("✅ Data saved. Goodbye!")


def main():
    """Entry point for the CLI application."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
