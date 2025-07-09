import os 
from pathlib import Path
import subprocess

print("Starting the custom app")

# Run the app now 
subprocess.run([f"bash /home/cdsw/custom_app/run.sh"], shell=True, check=True)
