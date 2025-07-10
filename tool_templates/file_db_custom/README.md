# SQL Queries into a File

This tool shows how to set up an SQL query interface to a file (currently tested for parquet or CSV files). An example parquet file is provided, `titanic.parquet`, and CSV file `sample1.csv` that can be used for testing.

Your agents must have awareness of the file to use as a database. For example, a query that the agent should make to the tool:

```
SELECT * from 'titanic.parquet' LIMIT 1;
```

This means that the actual DB file name (either CSV or parquet have been tested) needs to be provided in the Task, in the Conversation, or in the Agent's goal so the table name is available to the agent. For example, you can add this to an Agent's goal:

> For all SQL queries, you must use the table name of 'table1.csv'. This is the only table available. If you need information about the rows within this table, you can run a DESCRIBE 'table1.csv'.

![](./example.png)

## How to Use

* Pull in this entire tool into an Agent Studio tool following [this](../README.md) guide.
* Add any parquet and CSV files you want right to the tool directory next to `titanic.parquet`.
* Make sure your agent knows which table to pull out, either in the `Role`/`Goal`/`Backstory` or part of the conversation prompt itself.

In this example, see that `'titanic.parquet'` is explicitly mentioned in the conversation. You can customize this tool to have a specific parquet or CSV file to read from for example.
