import gradio as gr
import time
import os
import requests
import json
import base64

print("Starting up the custom app - main driver")

# Configuration
WORKFLOW_MODEL_ENDPOINT = "https://modelservice.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work/model?accessKey=m8222b8ritc5f1opfe98wfr9wqhun4nx"
OPS_ENDPOINT = "https://cai-agent-studio-ops-e53y41.ml-2cba638a-03a.eng-ml-i.svbr-nqvp.int.cldr.work/"
CDSW_APIV2_KEY = os.environ.get("CDSW_APIV2_KEY")

def run_workflow(inputs):
    """Execute workflow via direct HTTP request"""
    encoded_inputs = base64.b64encode(json.dumps(inputs).encode("utf-8")).decode("utf-8")
    
    response = requests.post(
        WORKFLOW_MODEL_ENDPOINT,
        json={
            "request": {
                "action_type": "kickoff",
                "kickoff_inputs": encoded_inputs
            }
        },
        headers={
            "Authorization": f"Bearer {CDSW_APIV2_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    result = response.json()
    return result["response"]["trace_id"]

def get_workflow_status(trace_id):
    """Poll workflow status via ops endpoint"""
    response = requests.get(
        f"{OPS_ENDPOINT}/events?trace_id={trace_id}",
        headers={"Authorization": f"Bearer {CDSW_APIV2_KEY}"}
    )
    
    events = response.json()

    status = {"complete": False, "output": None}
    if len(events) > 0 and events[-1]["type"] == "crew_kickoff_completed":
        status["complete"] = True
        status["output"] = events[-1].get("output")
    
    return status

def calculate(expression):
    """Process the expression and return result"""
    
    if not expression:
        return "Please enter an expression"
    
    # Start workflow
    trace_id = run_workflow({
        "expression": expression
    })

    # Poll for completion
    while True:
        print("getting status")
        time.sleep(1)
        status = get_workflow_status(trace_id)
        print(status)
        if status["complete"]:
            break

    return status["output"]

with gr.Blocks() as demo:
    gr.Markdown("## My Custom Agent Studio Calculator App")

    expression_input = gr.Textbox(label="Expression", placeholder="Enter a mathematical expression...")
    result_output = gr.Textbox(label="Result", interactive=False)
    
    calculate_btn = gr.Button("Calculate")
    
    calculate_btn.click(
        fn=calculate,
        inputs=[expression_input],
        outputs=[result_output]
    )
    
    expression_input.submit(
        fn=calculate,
        inputs=[expression_input],
        outputs=[result_output]
    )

demo.queue().launch(server_port=int(os.getenv("CDSW_APP_PORT", "7860")))