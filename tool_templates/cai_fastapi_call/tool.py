"""
Make an API call to a Cloudera AI Application that hosts a FastAPI endpoint.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
import json 
import argparse
from pathlib import Path
import requests
import os

ROOT_DIR = Path(__file__).parent


class UserParameters(BaseModel):
    url: str = Field(description="The full domain of the Cloudera AI Application to make the API call to.")


class ToolParameters(BaseModel):
    """
    Arguments of a tool call. These arguments are passed to this tool whenever
    an Agent calls this tool. The descriptions below are also provided to agents
    to help them make informed decisions of what to pass to the tool.
    """
    types: Literal["docs", "method"] = Field(description="Whether to return the OpenAPI definition, or run an HTTP method to use for the API call.", default="docs") 
    route: Optional[str] = Field(description="The route of the API endpoint to call.", default="/") 
    method: Optional[Literal["GET", "POST", "PUT", "DELETE"]] = Field(description="The actualHTTP method to use for the API call if type is of type 'method'", default="GET")
    body: Optional[str] = Field(description="The body to include in the API call.", default='')



def run_tool(config: UserParameters, args: ToolParameters) -> Any:
    """
    Main tool code logic. Anything returned from this method is returned
    from the tool back to the calling agent.
    """
    # Remove trailing slash from URL
    url = config.url
    if url.endswith('/'):
        url = url[:-1]

    if args.docs == "true" or args.docs == "True":
        response = requests.get(f"{url}/openapi.json", headers={'Authorization': f'Bearer {os.getenv("CDSW_APIV2_KEY")}'})
        docs = response.json()
        return docs

    # Add leading slash to route
    route = args.route
    if not route.startswith('/'):
        route = '/' + route

    if args.method == 'GET':
        response = requests.get(f"{url}{route}", headers={'Authorization': f'Bearer {os.getenv("CDSW_APIV2_KEY")}'})
    elif args.method == 'POST':
        response = requests.post(f"{url}{route}", json=json.loads(args.body if args.body else '{}'), headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {os.getenv("CDSW_APIV2_KEY")}'})
    elif args.method == 'PUT':
        response = requests.put(f"{url}{route}", json=json.loads(args.body if args.body else '{}'), headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {os.getenv("CDSW_APIV2_KEY")}'})
    elif args.method == 'DELETE':
        response = requests.delete(f"{url}{route}", headers={'Authorization': f'Bearer {os.getenv("CDSW_APIV2_KEY")}'})

    return response.json()




OUTPUT_KEY = "tool_output"
"""
When an agent calls a tool, technically the tool's entire stdout can be passed back to the agent.
However, if an OUTPUT_KEY is present in a tool's main file, only stdout content *after* this key is
passed to the agent. This allows us to return structured output to the agent while still retaining
the entire stdout stream from a tool! By default, this feature is enabled, and anything returned
from the run_tool() method above will be the structured output of the tool.
"""


if __name__ == "__main__":
    """
    Tool entrypoint. 
    
    The only two things that are required in a tool are the
    ToolConfiguration and ToolArguments classes. Then, the only two arguments that are
    passed to a tool entrypoint are "--tool-config" and "--tool-args", respectively. The rest
    of the implementation is up to the tool builder - feel free to customize the entrypoint to your 
    chosing!
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-params", required=True, help="Tool configuration")
    parser.add_argument("--tool-params", required=True, help="Tool arguments")
    args = parser.parse_args()
    
    # Parse JSON into dictionaries
    user_dict = json.loads(args.user_params)
    tool_dict = json.loads(args.tool_params)
    
    # Validate dictionaries against Pydantic models
    config = UserParameters(**user_dict)
    params = ToolParameters(**tool_dict)
    
    # Run the tool.
    output = run_tool(config, params)
    print(OUTPUT_KEY, output)