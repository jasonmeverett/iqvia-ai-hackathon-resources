# Tool Templates

This directory contains some tool templates that you can add to an Agent Studio agent.


## How to Add tools

* In Agent Studio, create a workflow and an Agent
* In the Agent configuration page, open Create or Edit Tools
* Create a new tool and name the tool something useful for your agent (for example, `CSV Reader`)
* Creating a new tool will create a new `requirements.txt` and `tool.py` file in your workflow's directory
* In this repository, go to the subdirectory of the tool template you'd like to add (for example, `csv_reader/`)
* Copy the `requirements.txt`, `tool.py`, and any other pertinent data files into the directory