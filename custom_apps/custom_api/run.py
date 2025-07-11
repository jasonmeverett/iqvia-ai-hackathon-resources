import subprocess

out = subprocess.run([f"bash /home/cdsw/custom_api/run.sh"], shell=True, check=True)
print(out)

print("App start script is complete.")
