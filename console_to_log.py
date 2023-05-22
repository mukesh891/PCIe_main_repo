import sys

def redirect_output_to_file(file_path="ep_logs/ep_checker.log"):
    sys.stdout = open(file_path, "w")

def reset_output():
    sys.stdout = sys.__stdout__

# Redirect standard output to the log file
redirect_output_to_file()

# Your code goes here...
print("This will be logged to ep_checke.log")

# Stop redirecting console output to the log file
reset_output()

# Your code goes here...
print("The console prints are printed in ep_checker.log file")

# Close the log file when you're done
sys.stdout.close()


