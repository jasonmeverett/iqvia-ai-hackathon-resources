"""
Write some markdown to a Word Doc .docx file.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
import json 
import argparse
from pathlib import Path
import pandas as pd
import sys
import os
import markdown
from html2docx import html2docx
from docx import Document


ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))
os.chdir(ROOT_DIR)

class UserParameters(BaseModel):
    pass 


class ToolParameters(BaseModel):
    """
    Arguments of a tool call. These arguments are passed to this tool whenever
    an Agent calls this tool. The descriptions below are also provided to agents
    to help them make informed decisions of what to pass to the tool.
    """
    output_file: str = Field(description="The local path to the docx file to write. example: 'report.docx'")
    markdown_content: str = Field(description="The markdown content to write to the word docx file.")


def run_tool(config: UserParameters, args: ToolParameters) -> Any:
    """
    Main tool code logic. Anything returned from this method is returned
    from the tool back to the calling agent.
    """

    # Create a Word document
    doc = Document()

    html = f"""
    <html>
    <head></head>
    <body>
        {markdown.markdown(args.markdown_content)}
    </body>
    </html>
    """

    # Convert HTML to DOCX
    buf = html2docx(html, title="My Title")

    # Save the document
    with open(args.output_file, "wb") as fp:
        fp.write(buf.getvalue())


    abspath = os.path.abspath(args.output_file)

    return {
        "directory": os.path.dirname(abspath),
    }


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