"""
Explore information related to Core annotation for drug targets (gene/proteins). 
Targets are defined based on EMBL-EBI Ensembl database and uses the Ensembl gene 
ID as the primary identifier. An Ensembl gene ID is considered potential drug target 
if included in the canonical assembly or if present alternative assemblies but encoding 
for a reviewed protein product according to the UniProt database. 
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

DB_FILE = "drug_targets.parquet"
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

# Change to the tool's directory so relative paths work
os.chdir(ROOT_DIR)


class UserParameters(BaseModel):
    max_rows: Optional[int] = Field(description="The maximum number of rows to return.", default=10)


class ToolParameters(BaseModel):
    """
    Arguments passed for each tool call.
    """
    describe: Optional[Literal[True, False, None]] = Field(description="Used to ONLY describe the database table. This is a boolean value to describe the database table.", default=False)
    column_names: Optional[str] = Field(description="The column names of the database to return. This is a comma separated list of column names. Can also be a wildcard (*) to return all columns. Can also be a COUNT() command.", default=None)
    filter_column_1: Optional[str] = Field(description="Optional filter 1: The column to filter on. This is the column name to filter on.", default='*')
    filter_operation_1: Optional[Literal['equal_to', 'contains', 'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'not_equal_to']] = Field(description="Optional filter 1: The operation to use for filtering. Specifies how to compare the filter column with the filter value.", default=None)
    filter_value_1: Optional[Any] = Field(description="Optional filter 1: The value to filter on. This is the value to compare against using the specified operation.", default=None)
    filter_column_2: Optional[str] = Field(description="Optional filter 2. The column to filter on. This is the column name to filter on.", default='*')
    filter_operation_2: Optional[Literal['equal_to', 'contains', 'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'not_equal_to']] = Field(description="Optional filter 2: The operation to use for filtering. Specifies how to compare the filter column with the filter value.", default=None)
    filter_value_2: Optional[Any] = Field(description="Optional filter 2: The value to filter on. This is the value to compare against using the specified operation.", default=None)
    filter_column_3: Optional[str] = Field(description="Optional filter 3. The column to filter on. This is the column name to filter on.", default='*')
    filter_operation_3: Optional[Literal['equal_to', 'contains', 'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'not_equal_to']] = Field(description="Optional filter 3: The operation to use for filtering. Specifies how to compare the filter column with the filter value.", default=None)
    filter_value_3: Optional[Any] = Field(description="Optional filter 3: The value to filter on. This is the value to compare against using the specified operation.", default=None)
    limit: Optional[int] = Field(description="The number of rows to return. This is the number of rows to return.", default=None)
    offset: Optional[int] = Field(description="The number of rows to offset by. This is the number of rows to offset by.", default=None)
    order_by: Optional[str] = Field(description="The column to order by. This is the column to order by.", default=None)
    order_direction: Optional[str] = Field(description="The direction to order by. This is the direction to order by (ASC or DESC).", default=None)
    group_by: Optional[str] = Field(description="The column to group by. This is the column to group by.", default=None)


def run_tool(config: UserParameters, args: ToolParameters) -> Any:
    """
    Main tool logic: run SQL query against the file.
    """
    try:
        if args.describe:
            result = duckdb.sql(f"DESCRIBE '{DB_FILE}'").to_df()
            return result.to_json(orient="records")
        
        # Map operation to SQL operator
        operation_map = {
            'equal_to': '=',
            'contains': 'LIKE',
            'less_than': '<',
            'greater_than': '>',
            'less_than_or_equal': '<=',
            'greater_than_or_equal': '>=',
            'not_equal_to': '!='
        }
        
        # Build SQL query
        columns = args.column_names if args.column_names != '*' else '*'

        # Handle contains operation specially
        filter_clause_1 = None
        if args.filter_operation_1:
            assert args.filter_value_1 is not None, "Filter value is required for contains operation"
            assert args.filter_column_1 is not None, "Filter column is required for contains operation"
            try:
                print("trying to parse filter_value as number")
                float(args.filter_value_1)
                filter_value = args.filter_value_1
            except Exception as e:
                print("Just using filter_value as string")
                filter_value = f"'{args.filter_value_1}'"
            filter_clause_1 = f"WHERE {args.filter_column_1} {operation_map[args.filter_operation_1]} {filter_value} "

        filter_clause_2 = None
        if args.filter_operation_2:
            assert args.filter_value_2 is not None, "Filter value is required for contains operation"
            assert args.filter_column_2 is not None, "Filter column is required for contains operation"
            try:
                print("trying to parse filter_value as number")
                float(args.filter_value_2)
                filter_value = args.filter_value_2
            except Exception as e:
                print("Just using filter_value as string")
                filter_value = f"'{args.filter_value_2}'"
            filter_clause_2 = f"AND {args.filter_column_2} {operation_map[args.filter_operation_2]} {filter_value} "

        filter_clause_3 = None
        if args.filter_operation_3:
            assert args.filter_value_3 is not None, "Filter value is required for contains operation"
            assert args.filter_column_3 is not None, "Filter column is required for contains operation"
            try:
                print("trying to parse filter_value as number")
                float(args.filter_value_3)
                filter_value = args.filter_value_3  
            except Exception as e:
                print("Just using filter_value as string")
                filter_value = f"'{args.filter_value_3}'"
            filter_clause_3 = f"AND {args.filter_column_3} {operation_map[args.filter_operation_3]} {filter_value}"

        sql_query = f"SELECT {columns} FROM '{DB_FILE}' " \
            + (filter_clause_1 if filter_clause_1 else "") \
            + (filter_clause_2 if filter_clause_2 else "") \
            + (filter_clause_3 if filter_clause_3 else "")

        # Add optional clauses
        if args.group_by:
            sql_query += f" GROUP BY {args.group_by}"
        
        if args.order_by:
            direction = args.order_direction if args.order_direction else 'ASC'
            sql_query += f" ORDER BY {args.order_by} {direction}"
        
        max_rows = config.max_rows if config.max_rows else 10
        if args.limit:
            sql_query += f" LIMIT {args.limit}"
        else:
            sql_query += f" LIMIT {max_rows}"

        if args.offset:
            sql_query += f" OFFSET {args.offset}"
        
        # Run SQL with DuckDB
        print(f"Running SQL query: {sql_query}")
        result = duckdb.sql(sql_query).to_df()
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
