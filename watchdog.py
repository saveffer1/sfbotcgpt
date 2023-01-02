print("Watchdog start:")
while True: # run forever
    print("Watchdog: process started")  # program started message
    exec(open("./program.py").read())   # run the program
    print("Watchdog: process finished") # program stopped message
print("Watchdog end:") # the watchdog is now finishing
