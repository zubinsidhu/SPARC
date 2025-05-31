import time
import sys

def set(time_str):
    """
    Counts down from a specified time in HH:MM:SS format.

    Args:
        time_str (str): The time to count down from in HH:MM:SS format.
    """
    
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        if not (0 <= hours <= 99 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
            print("Invalid time format. Hours should be between 00 and 99, minutes and seconds between 00 and 59.")
            return

        while total_seconds > 0:
            timer = divmod(total_seconds, 60)
            hours = timer[0] // 60
            minutes = timer[0] % 60
            seconds = timer[1]
            sys.stdout.write(f"\r{hours:02d}:{minutes:02d}:{seconds:02d}")
            sys.stdout.flush()
            time.sleep(1)
            total_seconds -= 1

        print("\rTime's up!          ")

    except ValueError:
        print("Invalid time format. Please use HH:MM:SS.")

if __name__ == "__main__":
    set(time_str="00:10:00")
