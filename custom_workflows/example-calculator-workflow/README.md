# Agent Studio Custom Workflow Example

This is a custom workflow that can be deployed to Agent Studio. This example demonstrates how to create and deploy a workflow with custom tools and agents.

**NOTE: update `github_url` in `deploy.sh` to match wherever you push your repo.**

## Overview

This project contains:
- A baseline workflow specification (`workflow.yaml`) that references the input configuration. Currently only `collated_input` types are supported.
- A custom calculator tool (`calculator_tool/`) with Python implementation
- A workflow configuration (`collated_input.json`) that defines the complete workflow structure, agents, etc.
- A deployment script (`deploy.sh`) as an example for deploying to Agent Studio

## Workflow Structure

Currently, you can only deploy `collated_input` types. The workflow is defined using a JSON structure that includes:

- **Language Models**: Configuration for LLM providers (OpenAI GPT-4 in this example)
- **Tool Instances**: Custom tools with Python code, requirements, and metadata
- **Agents**: AI agents with specific roles, goals, and assigned tools
- **Tasks**: Specific tasks to be executed by agents
- **Workflow**: Overall workflow configuration and execution process

## Example Structure

See the example `collated_input.json` for how to structure this input. The structure includes:

```json
{
  "default_language_model_id": "m1",
  "language_models": [...],
  "tool_instances": [...],
  "agents": [...],
  "tasks": [...],
  "workflow": {...}
}
```

### Key Components:

1. **Language Models**: Define the LLM configurations with generation parameters
2. **Tool Instances**: Custom Python tools with their source code and dependencies
3. **Agents**: CrewAI-based agents with roles, backstories, and assigned tools
4. **Tasks**: Specific tasks with descriptions and expected outputs
5. **Workflow**: The overall workflow orchestration

## Deploying

### Prerequisites

Set up your environment variables for deployment:

```bash
export CDSW_APIV2_KEY="your-api-key-here"
export MY_AGENT_STUDIO_URL="https://your-agent-studio-url.com"
export MY_LLM_API_KEY="your-llm-api-key-here"
```

### Deployment Process

See `deploy.sh` as an example of how to deploy to an Agent Studio's `/api/deploy` route. The deployment script:

1. Sets up the required environment variables
2. Creates a JSON payload with:
   - Workflow target configuration
   - Deployment target settings (workbench model configuration)
   - Deployment configuration (generation and LLM settings)
3. Makes a POST request to the Agent Studio API endpoint

### Running the Deployment

```bash
# Run the deployment
./deploy.sh
```

### Environment Variables

Populate your environment variables as you see fit for testing deployment:

- `CDSW_APIV2_KEY`: Your Agent Studio API key
- `MY_AGENT_STUDIO_URL`: The URL of your Agent Studio instance
- `MY_LLM_API_KEY`: Your LLM provider API key (Either CAII JWT Token, OpenAI API key, etc.)

**DON'T FORGET TO UPDATE YOUR LLM TYPE IF NECESSARY.**

Example:
```
        "llm_config": {
            "m1": {
                "model_type": "CAII",
                "provider_model": "<input model identifier here>",
                "api_base": "<api base of CAI model>",
                "api_key": "${MY_LLM_API_KEY}"
            }
        }
```

## Custom Tools

The example includes a calculator tool in the `calculator_tool/` directory:
- `tool.py`: Main tool implementation
- `requirements.txt`: Python dependencies
- `icon.png`: Tool icon
- `calc.py`: Supporting calculation logic

## Workflow Configuration

The `workflow.yaml` file specifies:
- Input file: `collated_input.json`
- Type: `collated_input`

This tells Agent Studio how to interpret and deploy your workflow configuration.

## Testing

After deployment, your workflow will be available in Agent Studio and can process mathematical expressions using the calculator agent and tool.
