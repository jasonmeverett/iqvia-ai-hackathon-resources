"""
Activate all tool templates for this repo into a given agent studio instance. This script
can be run anywhere within an agent studio project to activate all of these tool templates.
"""

import requests 
import shutil 
import os 
import json
from pathlib import Path

agent_studio_dir = "/home/cdsw"
if os.path.exists("/home/cdsw/agent-studio"):
    agent_studio_dir = "/home/cdsw/agent-studio"

# Get this dir
curdir = os.path.abspath(str(Path(__file__).parent))
print(f"Current directory: {curdir}")

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

# Activate tool templates
for tool_template in manifest['tool_templates']:
    
    as_tool_template: dict = {}
    tool_template_id: str = ""

    # See if the ID of this tool template is in the current tool templates
    if tool_template['name'] in [x['name'] for x in current_tool_templates]:
        print(f"Tool template {tool_template['name']} already exists")
        tool_template_id = [x['id'] for x in current_tool_templates if x['name'] == tool_template['name']][0]
    else:
        print(f"Tool template {tool_template['name']} does not exist")

        payload = {
            "tool_template_name": tool_template['name'],
        }
        print(f"Checking for icon.png in {os.path.join(curdir, tool_template['directory'])}")
        if os.path.exists(os.path.join(curdir, tool_template['directory'], "icon.png")):
            payload['tmp_tool_image_path'] = os.path.join(curdir, tool_template['directory'], "icon.png")

        print(f"Payload: {payload}")

        # Activate the tool template
        data = requests.post(
            f"{agent_studio_endpoint}/api/grpc/addToolTemplate",
            json=payload,
            headers={
                "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
            }
        ).json()
        print(data)
        tool_template_id = data['tool_template_id']
    
    as_tool_template = requests.get(
        f"{agent_studio_endpoint}/api/grpc/getToolTemplate?tool_template_id={tool_template_id}",
        headers={
            "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
        }
    ).json()["template"]

    # Copy the tool template to the agent studio directory
    shutil.copytree(f"{tool_template['directory']}", os.path.join(agent_studio_dir, as_tool_template['source_folder_path']), dirs_exist_ok=True)