from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/healthz")
def health_check():
    return JSONResponse(content={"status": "ok"})

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the dummy FastAPI service!", "data": {"value": 42}})

import os

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("CDSW_APP_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
