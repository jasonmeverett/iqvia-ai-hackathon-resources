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

def serialize_conversation_history(history):
    """Convert conversation history to serialized string format"""
    if not history:
        return ""
    
    serialized = []
    for user_msg, assistant_msg in history:
        serialized.append(f"User: {user_msg}")
        if assistant_msg:
            serialized.append(f"Assistant: {assistant_msg}")
    
    return "\n".join(serialized)

def chat_response(message, history):
    """Process the user message and return response"""
    
    if not message:
        return history, ""
    
    # Serialize conversation history for context
    context = serialize_conversation_history(history)
    
    # Start workflow with user input and context
    trace_id = run_workflow({
        "user_input": message,
        "context": context
    })

    # Poll for completion
    while True:
        print("getting status")
        time.sleep(1)
        status = get_workflow_status(trace_id)
        print(status)
        if status["complete"]:
            break

    response = status["output"] if status["output"] else "I apologize, but I couldn't process your request."
    
    # Add the conversation to history
    history.append((message, response))
    
    return history, ""

with gr.Blocks() as demo:
    gr.Markdown("## My Custom Agent Studio Chat App")

    chatbot = gr.Chatbot(label="Conversation", height=500)
    msg = gr.Textbox(label="Message", placeholder="Type your message here...")
    
    clear_btn = gr.Button("Clear Chat")
    
    msg.submit(
        fn=chat_response,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )
    
    clear_btn.click(
        fn=lambda: ([], ""),
        outputs=[chatbot, msg]
    )

demo.queue().launch(server_port=int(os.getenv("CDSW_APP_PORT", "7860")))