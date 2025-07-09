# Conversation App

Example of a conversation application that uses a deployed Agent Studio conversational workflow.


## How to install this application
* In an Agent Studio instance, open Agent Studio and deploy the Calculator Workflow. 
* In an Agent Studio enabled project, make a directory named `custom_app/` from the home directory.
* You should now have:

```
agent-studio/
custom_app/
```

* Download `conversation_app.tar.gz` from this repo, and upload this tarball to your project filesystem (the root should be `/home/cdsw`)
* Start a new session in your project
* In your session terminal, extract all with `tar -xzvf conversation_app.tar.gz`
* You should now have:

```
agent-studio/
custom_app/
|_ main.py
|_ run.py
|_ run.sh
|_ pyproject.toml
|_ uv.lock
```

* in `main.py`, populate the remaining environment variables you need:
  * for `WORKFLOW_MODEL_ENDPOINT`, pull the model endpoint (with access key) that you can find in the Model Deployments page
    * looks like: `https://modelservice.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work/model?accessKey=m8222b8ritc5f1opfe98wfr9wqhun4nx`
  * for `OPS_ENDPOINT`, put the nominal URL of the Agent Studio - Agent Ops & Metrics application
    * looks like: `https://cai-agent-studio-ops-e53y41.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work/`
* In the Agent Studio project, under `Applications`, create a new application
* Under script, put `custom_app/run.py`
* Start the application

With luck, your application should spin up properly and be available for you to open and use.