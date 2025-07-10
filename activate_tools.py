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
applications: list[dict] = resp.json()['applications']
print(applications)

agent_studio_application_candidates = list(filter(lambda x: x['name'] == "Agent Studio", applications))
assert len(agent_studio_application_candidates) == 1, "There should be exactly one Agent Studio application in the project"
agent_studio_endpoint = f"https://{agent_studio_application_candidates[0]['subdomain']}.{os.getenv('CDSW_DOMAIN')}"
print(f"Agent Studio endpoint: {agent_studio_endpoint}")

# Get current tool templates
resp = requests.get(
    f"{agent_studio_endpoint}/api/grpc/listToolTemplates",
    headers={
        "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
    }
)
current_tool_templates: list[dict] = resp.json()['templates']
print(current_tool_templates)

# Activate tool templates
for tool_template in manifest['tool_templates']:
    print(f"Activating tool template: {tool_template['name']}")