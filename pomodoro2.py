import os
import platform
import time
import threading
import sys
from playsound import playsound 

# Constants for Pomodoro Timer
WORK_TIME = 1 * 60  # 25 minutes in seconds
POMODORO_COUNT = 4  # Number of Pomodoros before a long break

# Lists to store tasks and completed Pomodoros
tasks = []
completed_pomodoros = []

# Function to display countdown timer in clock-like format
def countdown_timer(seconds):
    while seconds:
        minutes, secs = divmod(seconds, 60)
        time_format = '{:02d}:{:02d}'.format(minutes, secs)
        sys.stdout.write("\rTime Remaining: " + time_format)
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    print("\rTime Remaining: 00:00")  # Display 00:00 when timer reaches 0
    playsound("C:\\Users\\HOME\\Downloads\\clock-alarm-8761.mp3")
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        

# Function to get user input for break time
def get_break_time():
    while True:
        try:
            break_time = int(input("Enter break time in minutes (or 0 for default 5 minutes): "))
            if break_time < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer or 0.")
    return break_time * 60  # Convert minutes to seconds

# Function to start the Pomodoro Timer
def start_pomodoro():
    # Change hosts path based on your operating system
    system_name = platform.system()
    if system_name == "Windows":
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    elif system_name == "Linux":
        hosts_path = "/etc/hosts"
    else:
        print("Unsupported operating system.")
        exit()

    # List of websites to block
    website_list = ["www.facebook.com", "facebook.com", "www.youtube.com", "youtube.com"]

    # IP address to redirect to (in this case, localhost)
    redirect_ip = "127.0.0.1"
    pomodoro_count = 0

    while True:
        task = input("Enter a task to do (or 'q' to quit): ")
        if task.lower() == 'q':
            break

        tasks.append(task)
        print("Task added:", task)

       
        # Get user input for break time
        break_time = get_break_time()
       
         # Block the websites
        with open(hosts_path, "r+") as hosts_file:
            content = hosts_file.read()
            for website in website_list:
                if website not in content:
                    hosts_file.write(redirect_ip + " " + website + "\n")
                    

        # Start the timer for work time
        print("Pomodoro started for 1 minutes.")
        print("The websites are blocked")
        t = threading.Thread(target=countdown_timer, args=(WORK_TIME,))
        t.start()
        t.join()
        print("Task completed:", task)

        completed_pomodoros.append(task)
        pomodoro_count += 1
        # Unblock websites during break time
        with open(hosts_path, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
            file.truncate()
           

        # Take a short break after completing a Pomodoro
        if pomodoro_count % POMODORO_COUNT == 0:
            print("Take a long break for {} minutes.".format(break_time // 60))
            print("The websites are unblocked")
            t = threading.Thread(target=countdown_timer, args=(break_time,))
            t.start()
            t.join()
            print("Long break completed.")
        else:
            print("Take a short break for {} minutes.".format(break_time // 60))
            print("The websites are unblocked")
            t = threading.Thread(target=countdown_timer, args=(break_time,))
            t.start()
            t.join()
            print("Short break completed.")
        playsound("C:\\Users\\HOME\\Downloads\\clock-alarm-8761.mp3")
    print("Tasks completed:")
    for task in completed_pomodoros:
        print("- " + task)


# Start the Pomodoro timer
start_pomodoro()
# Check every 5 seconds
time.sleep(5)



