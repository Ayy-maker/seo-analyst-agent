"""
Automated Scheduler - Run SEO reports automatically
"""

import schedule
import time
import subprocess
from datetime import datetime
from pathlib import Path
import os


class SEOScheduler:
    """Schedule automatic SEO report generation"""
    
    def __init__(self, project_dir: str = None):
        """
        Initialize scheduler
        
        Args:
            project_dir: Path to SEO project directory
        """
        self.project_dir = project_dir or str(Path(__file__).parent.parent)
    
    def run_analysis(self, client_name: str = None):
        """Run SEO analysis"""
        print(f"\n{'='*60}")
        print(f"🚀 Running scheduled SEO analysis")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if client_name:
            print(f"Client: {client_name}")
        print(f"{'='*60}\n")
        
        try:
            # Run analysis script
            script_path = Path(self.project_dir) / 'run_analysis.sh'
            result = subprocess.run([str(script_path)], 
                                  cwd=self.project_dir,
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                print("✅ Analysis completed successfully")
                print(result.stdout)
            else:
                print("❌ Analysis failed")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error running analysis: {e}")
    
    def schedule_monthly(self, day: int = 1, hour: int = 9, minute: int = 0):
        """
        Schedule monthly reports
        
        Args:
            day: Day of month (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
        """
        # Note: schedule library doesn't support monthly directly
        # So we check daily if it's the target day
        def check_and_run():
            if datetime.now().day == day:
                self.run_analysis()
        
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(check_and_run)
        print(f"📅 Scheduled: Monthly on day {day} at {hour:02d}:{minute:02d}")
    
    def schedule_weekly(self, day: str = 'monday', hour: int = 9, minute: int = 0):
        """
        Schedule weekly reports
        
        Args:
            day: Day of week (monday, tuesday, etc.)
            hour: Hour (0-23)
            minute: Minute (0-59)
        """
        day_func = getattr(schedule.every(), day.lower())
        day_func.at(f"{hour:02d}:{minute:02d}").do(self.run_analysis)
        print(f"📅 Scheduled: Weekly on {day.title()} at {hour:02d}:{minute:02d}")
    
    def schedule_daily(self, hour: int = 9, minute: int = 0):
        """
        Schedule daily reports
        
        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
        """
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self.run_analysis)
        print(f"📅 Scheduled: Daily at {hour:02d}:{minute:02d}")
    
    def run(self):
        """Start the scheduler (runs forever)"""
        print("\n🤖 SEO Scheduler Started")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n👋 Scheduler stopped")


# CLI usage
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Schedule automated SEO reports')
    parser.add_argument('--monthly', type=int, metavar='DAY', 
                       help='Schedule monthly on this day (1-31)')
    parser.add_argument('--weekly', choices=['monday', 'tuesday', 'wednesday', 
                                            'thursday', 'friday', 'saturday', 'sunday'],
                       help='Schedule weekly on this day')
    parser.add_argument('--daily', action='store_true', 
                       help='Schedule daily')
    parser.add_argument('--hour', type=int, default=9,
                       help='Hour to run (0-23, default: 9)')
    parser.add_argument('--minute', type=int, default=0,
                       help='Minute to run (0-59, default: 0)')
    parser.add_argument('--now', action='store_true',
                       help='Run immediately once')
    
    args = parser.parse_args()
    
    scheduler = SEOScheduler()
    
    if args.now:
        scheduler.run_analysis()
    elif args.monthly:
        scheduler.schedule_monthly(args.monthly, args.hour, args.minute)
        scheduler.run()
    elif args.weekly:
        scheduler.schedule_weekly(args.weekly, args.hour, args.minute)
        scheduler.run()
    elif args.daily:
        scheduler.schedule_daily(args.hour, args.minute)
        scheduler.run()
    else:
        print("Please specify --monthly, --weekly, --daily, or --now")
        print("Example: python scheduler.py --monthly 1 --hour 9")
