import os

log_path = os.path.abspath('logs/app.log')
print(f"Log path: {log_path}")
print(f"Directory exists: {os.path.exists('logs')}")
print(f"Log file exists: {os.path.exists(log_path)}")
print(f"Can write to directory: {os.access('logs', os.W_OK)}")
print(f"Can write to file: {os.access(log_path, os.W_OK)}")
