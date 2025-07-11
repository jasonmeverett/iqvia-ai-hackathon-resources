# Custom FastAPI as an Application

Cloudera AI can be used to host custom FastAPI endpoints. These endpoints, if they're signed with `Authorization: Bearer $CDSW_APIV2_KEY`, can be used like any generic FastAPI endpoint.

This package ships with an example of how to enable this. In order to activate a template Custom API, follow these steps:

* Start up a session within an existing Agent Studio instance
* Once the session starts, open a terminal under "New Terminal", seen in the top menu bar of the session window
* Run this in a terminal:

```
git clone https://github.com/jasonmeverett/iqvia-ai-hackathon-resources.git
```

* Enter into the directory:

```
cd iqvia-ai-hackathon-resources/
```

* Activate the template for your custom API with

```
python activate_custom_api.py
```

You'll now notice that there is a new app, "Custom API", that is serving a FastAPI endpoint. If you want to make changes to this api, you can make changes to the `custom_api/api.py` file from within your project.

NOTE: if you run `python activate_custom_api.py` more than once, you may lose any changes you make to `api.py`

### Calling custom API from Agent Studio

If you follow the steps to install custom tools above, you'll notice a tool named `Make API Call to Cloudera AI FastAPI Application`. Add this tool to an Agent, and specify the URL of the new application you just made.

When you run the `activate_custom_api.py` script you should notice this output:

```
...
You can access your API at: https://custom-api.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work       <------------ THIS IS THE ONE YOU WANT
You can access your API docs at: https://custom-api.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work/docs
You can access your API OpenAPI definition at: https://custom-api.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work/openapi.json
```

You can use the first URL as the configuration to the tool.