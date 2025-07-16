"""
Run specific SQL queries against a database table. An optional describe feature is also provided to pull out to view table schema.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional, Literal
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
    """
    User parameters for the tool.
    """
    db_file: str = Field(description="The path to the database file to use for the query. Currently only CSV and Parquet files are supported.")

#1st replacement
class ToolParameters(BaseModel):
    """
    Arguments passed for each tool call.
    """
    describe: Optional[Literal[True, False, None]] = Field(description="Used to ONLY describe the database table. This is a boolean value to describe the database table.", default=False)
    calculated_fields: Optional[str] = Field(description="Comma-separated list of calculated fields. Example: \"(Received_Date - Collection_Date) AS transit_time, Collection_Date + INTERVAL '7 days' AS week_later\"", default=None)
    column_names: Optional[str] = Field(description="The column names of the database to return. This is a comma separated list of column names. Can also be a wildcard (*) to return all columns. Can also be a COUNT() command.", default=None)
    where_clause: Optional[str] = Field(description="SQL WHERE clause without the WHERE keyword. Example: \"Received_State = 'Ambient' OR Received_State = 'Refrigerated'\"", default=None)
    limit: Optional[int] = Field(description="The number of rows to return. This is the number of rows to return.", default=None)
    offset: Optional[int] = Field(description="The number of rows to offset by. This is the number of rows to offset by.", default=None)
    order_by: Optional[str] = Field(description="The column to order by. This is the column to order by.", default=None)
    order_direction: Optional[str] = Field(description="The direction to order by. This is the direction to order by (ASC or DESC).", default=None)
    group_by: Optional[str] = Field(description="The column to group by. This is the column to group by.", default=None)
    output_file: Optional[str] = Field(description="Optional path to save the query result as a new CSV or Parquet file.", default=None)


#2nd replacement
def run_tool(config: UserParameters, args: ToolParameters) -> Any:
    """
    Main tool logic: run SQL query against the file.
    """
    try:
        if args.describe:
            result = duckdb.sql(f"DESCRIBE '{config.db_file}'").to_df()
            return result.to_json(orient="records")

        # Build column list with calculated fields
        columns = args.column_names if args.column_names else '*'
        if args.calculated_fields:
            if columns == '*':
                columns = '*, ' + args.calculated_fields
            else:
                columns = columns + ', ' + args.calculated_fields
        
        sql_query = f"SELECT {columns} FROM '{config.db_file}'"
        
        # Add WHERE clause if provided
        if args.where_clause:
            sql_query += f" WHERE {args.where_clause}"
        
        # Add optional clauses
        if args.group_by:
            sql_query += f" GROUP BY {args.group_by}"
        
        if args.order_by:
            direction = args.order_direction if args.order_direction else 'ASC'
            sql_query += f" ORDER BY {args.order_by} {direction}"
        
        if args.limit:
            sql_query += f" LIMIT {args.limit}"
        
        if args.offset:
            sql_query += f" OFFSET {args.offset}"
        
        # Run SQL with DuckDB
    # removed
        print(f"Running SQL query: {sql_query}")
        result = duckdb.sql(sql_query).to_df()

        # Check if an output file path is provided
        if args.output_file:
            # Save the result to the specified file
            if args.output_file.endswith('.csv'):
                result.to_csv(args.output_file, index=False)
            elif args.output_file.endswith('.parquet'):
                result.to_parquet(args.output_file, index=False)
            else:
                return json.dumps({"error": "Output file must be .csv or .parquet"}, indent=2)
            
            # Return a success message instead of the data
            return json.dumps({"success": f"Data successfully saved to {args.output_file}"}, indent=2)
        else:
            # If no output file, return the data as JSON (for small, aggregated queries)
            return result.to_json(orient="records", indent=2)
            
        # print(f"Running SQL query: {sql_query}")
        # result = duckdb.sql(sql_query).to_df()
        # return result.to_json(orient="records", indent=2)

    
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
