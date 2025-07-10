"""
A simple SQL query tool that can run any SQL query against a Parquet or CSV file. The Parquet or CSV file
should be used as the table name (example: SELECT * FROM file.parquet LIMIT 1;)
"""

from pydantic import BaseModel, Field
from typing import Any
import json
import argparse
from pathlib import Path
import pandas as pd
import duckdb
import sys 
import os

ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

# Change to the tool's directory so relative paths work
os.chdir(ROOT_DIR)


class UserParameters(BaseModel):
    pass


class ToolParameters(BaseModel):
    """
    Arguments passed for each tool call.
    """
    sql: str = Field(description="The SQL query to run on the specified file, with the table name being the name of the file.")


def run_tool(config: UserParameters, args: ToolParameters) -> Any:
    """
    Main tool logic: run SQL query against the file.
    """
    try:
        # Run SQL with DuckDB
        result = duckdb.sql(f"{args.sql}").to_df()
        return result.to_json(orient="records", indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


OUTPUT_KEY = "tool_output"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-params", required=True, help="Tool configuration")
    parser.add_argument("--tool-params", required=True, help="Tool arguments")
    args = parser.parse_args()

    user_dict = json.loads(args.user_params)
    tool_dict = json.loads(args.tool_params)

    config = UserParameters(**user_dict)
    params = ToolParameters(**tool_dict)

    output = run_tool(config, params)
    print(OUTPUT_KEY, output)
