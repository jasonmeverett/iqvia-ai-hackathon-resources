"""
Deploys a simple API as an application and adds files to /home/cdsw/custom_api for running it.
"""
import requests
import os
from pathlib import Path
import shutil
import cmlapi 


APPLICATION_SUBDOMAIN = "custom-api"
APPLICATION_NAME = "Custom API"
APPLICATION_DIR = "/home/cdsw/custom_api"


# Copy over # Get this dir
curdir = os.path.abspath(str(Path(__file__).parent))
print(f"Current directory: {curdir}")

# Copy over the files for the custom application
if os.path.exists(APPLICATION_DIR):
    print(f"WARNING:Application directory {APPLICATION_DIR} already exists!!")
    print(f"WARNING:Will copy {APPLICATION_DIR}/api.py to {APPLICATION_DIR}/api.backup.py just in case you want to restore it.")
    shutil.copy(os.path.join(APPLICATION_DIR, "api.py"), os.path.join(APPLICATION_DIR, "api.backup.py"))


shutil.copytree(os.path.join(curdir, "custom_apps", "custom_api"), APPLICATION_DIR, dirs_exist_ok=True)



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
as_application: dict = agent_studio_application_candidates[0]
print(as_application)
runtime_identifier = as_application['runtime_identifier']



# Grab the application if it already exists
resp = requests.get(
    f"https://{os.getenv('CDSW_DOMAIN')}/api/v2/projects/{os.getenv('CDSW_PROJECT_ID')}/applications?page_size=10000", 
    headers={
        "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
    }
)
applications: list[dict] = resp.json()['applications']

api_application_candidates = list(filter(lambda x: x['name'] == APPLICATION_NAME, applications))

# If the application doesn't exist, create it
if len(api_application_candidates) == 0:
    # Create the application
    print("Creating application")
    resp = requests.post(
        f"https://{os.getenv('CDSW_DOMAIN')}/api/v2/projects/{os.getenv('CDSW_PROJECT_ID')}/applications",
        headers={
            "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
        },
        json={
            "name": APPLICATION_NAME,
            "runtime_identifier": runtime_identifier,
            "subdomain": APPLICATION_SUBDOMAIN,
            "cpu": 2,
            "memory": 4,
            "description": "Custom FastAPI served as a CAI Application",
            "project_id": os.getenv('CDSW_PROJECT_ID'),
            "script": "custom_api/run.py"
        }
    )
    application = resp.json()
    print(application)
    print(f"APPLICATION CREATED")
    print(f"You can access your API at: https://{application['subdomain']}.{os.getenv('CDSW_DOMAIN')}")
    print(f"You can access your API docs at: https://{application['subdomain']}.{os.getenv('CDSW_DOMAIN')}/docs")
    print(f"You can access your API OpenAPI definition at: https://{application['subdomain']}.{os.getenv('CDSW_DOMAIN')}/openapi.json")

# If it does exist, restart it
else:
    print("Application already exists, restarting it")
    assert len(api_application_candidates) == 1, "There should be exactly one Agent Studio application in the project"
    resp = requests.post(
        f"https://{os.getenv('CDSW_DOMAIN')}/api/v2/projects/{os.getenv('CDSW_PROJECT_ID')}/applications/{api_application_candidates[0]['id']}:restart",
        headers={
            "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
        }
    )
    print(resp.json())
    print("Application restarted")
    print(f"You can access your API at: https://{api_application_candidates[0]['subdomain']}.{os.getenv('CDSW_DOMAIN')}")
    print(f"You can access your API docs at: https://{api_application_candidates[0]['subdomain']}.{os.getenv('CDSW_DOMAIN')}/docs")
    print(f"You can access your API OpenAPI definition at: https://{api_application_candidates[0]['subdomain']}.{os.getenv('CDSW_DOMAIN')}/openapi.json")