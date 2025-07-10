import requests 
import shutil 
import os 
import json
from pathlib import Path

agent_studio_dir = "/home/cdsw"
if os.path.exists("/home/cdsw/agent-studio"):
    agent_studio_dir = "/home/cdsw/agent-studio"

# Copy tool templates
curdir = str(Path(__file__).parent)
shutil.copytree(f"{curdir}/tool_templates/", f"{agent_studio_dir}/studio-data/tool_templates/", dirs_exist_ok=True)

# Load the manifest.json file
manifest_file = f"manifest.json"
manifest = {}
with open(manifest_file, "r") as f:
    manifest = json.load(f)

# Grab the agent studio url
resp = requests.get(
    f"https://{os.getenv('CDSW_DOMAIN')}/api/v2/projects/{os.getenv('CDSW_PROJECT_ID')}/applications?page_size=10000", 
    headers={
        "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
    }
)
applications = resp.json()
print(applications)