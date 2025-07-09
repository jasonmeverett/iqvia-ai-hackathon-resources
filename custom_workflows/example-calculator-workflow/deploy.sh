#!/bin/bash

# SECRET KEYS that need to be stored as part of a jenkins job or GH action

# Used for authorization when calling the Agent Studio API
MY_CDSW_APIV2_KEY=

# Agent studio URL endpoint
MY_AGENT_STUDIO_URL=

# Used for the LLM API key
MY_LLM_API_KEY= 

# Deployment payload of the artifact
read -r -d '' PAYLOAD <<EOF
{
    "workflow_target": {
        "workflow_name": "Example Calculator Workflow #1",
        "type": "github",
        "github_url": "https://github.com/jasonmeverett/agent-studio-example-workflow"
    },
    "deployment_target": {
        "type": "workbench_model",
        "auto_redeploy_to_type": true,
        "workbench_resource_profile": {
            "cpu": 2,
            "mem": 4,
            "num_replicas": 1
        }
    },
    "deployment_config": {
        "generation_config": {
            "temperature": 0.1,
            "max_new_tokens": 5
        },
        "llm_config": {
            "m1": {
                "model_type": "OPENAI",
                "provider_model": "gpt-4o",
                "api_key": "${MY_LLM_API_KEY}"
            }
        }
    }
}
EOF

# Actual Agent Studio API call
curl -X POST $MY_AGENT_STUDIO_URL/api/deploy \
  -H "Authorization: Bearer $MY_CDSW_APIV2_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"