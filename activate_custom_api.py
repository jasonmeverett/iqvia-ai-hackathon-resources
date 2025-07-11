"""
Deploys a simple API as an application and adds files to /home/cdsw/custom_api for running it.
"""
import requests
import os
from pathlib import Path
import shutil
import cmlapi 


APPLICATION_NAME = "Custom API"
APPLICATION_DIR = "/home/cdsw/custom_api"


# Copy over # Get this dir
curdir = os.path.abspath(str(Path(__file__).parent))
print(f"Current directory: {curdir}")

# Copy over the files for the custom application
shutil.copytree(os.path.join(curdir, "custom_apps", "custom_api/"), APPLICATION_DIR, dirs_exist_ok=True)





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
as_application: cmlapi.Application = agent_studio_application_candidates[0]
runtime = as_application.runtime











# # Grab the application if it already exists
# resp = requests.get(
#     f"https://{os.getenv('CDSW_DOMAIN')}/api/v2/projects/{os.getenv('CDSW_PROJECT_ID')}/applications?page_size=10000", 
#     headers={
#         "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
#     }
# )
# applications: list[dict] = resp.json()['applications']

# api_application_candidates = list(filter(lambda x: x['name'] == APPLICATION_NAME, applications))

# # If the application doesn't exist, create it
# if len(api_application_candidates) == 0:
#     # Create the application
#     resp = requests.post(
#         f"https://{os.getenv('CDSW_DOMAIN')}/api/v2/projects/{os.getenv('CDSW_PROJECT_ID')}/applications",
#         headers={
#             "Authorization": f"Bearer {os.getenv('CDSW_APIV2_KEY')}"
#         }
#     )
# # If it does exist, restart it
# else:
#     assert len(api_application_candidates) == 1, "There should be exactly one Agent Studio application in the project"
#     api_application_endpoint = f"https://{api_application_candidates[0]['subdomain']}.{os.getenv('CDSW_DOMAIN')}"
#     print(f"API application endpoint: {api_application_endpoint}")




# # Create the application


