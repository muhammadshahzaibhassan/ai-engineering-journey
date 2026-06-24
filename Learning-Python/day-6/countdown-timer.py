import time


usertime = int(input("Enter the time in seconds: "))

for x in reversed(range(1, usertime + 1)):
    seconds = x % 60
    minutes = int(x / 60) % 60
    hours = int(x / 3600) % 60
    print(f"{hours:02}:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("Time's UP")